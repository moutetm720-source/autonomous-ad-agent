#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Sauvegarde Qdrant — VERSION CORRIGÉE (et réellement chiffrée)
#
# Corrections par rapport au script du plan initial :
#   1. BUG BLOQUANT : `.../collections/{COLLECTION_NAME}/snapshots` — le `$`
#      manquait, l'URL contenait le nom de la variable en littéral. Le snapshot
#      n'était donc jamais créé et le script sortait en erreur à chaque run.
#   2. Le script s'appelait « chiffré » mais ne chiffrait rien : c'était un
#      simple tar.gz. On chiffre ici avec `age` (moderne, simple) et on garde
#      une clé hors du serveur.
#   3. `grep -o` pour extraire le nom du snapshot : fragile. On utilise jq,
#      et on vérifie le code HTTP.
#   4. `sleep 3` en espérant que le snapshot soit prêt : on interroge le statut
#      jusqu'à completion (avec timeout).
#   5. Aucune copie hors site : une sauvegarde sur le même disque n'en est pas
#      une. On pousse sur un bucket S3/R2 (incrémental, quelques centimes).
#   6. Rotation 30 jours sans vérification d'espace disque.
# ---------------------------------------------------------------------------
set -euo pipefail

QDRANT_HOST="${QDRANT_HOST:-localhost}"
QDRANT_PORT="${QDRANT_PORT:-6333}"
QDRANT_API_KEY="${QDRANT_API_KEY:-}"
COLLECTION_NAME="${COLLECTION_NAME:-agence_connaissances}"
BACKUP_DIR="${BACKUP_DIR:-/app/agence_workspace/backups}"
AGE_RECIPIENT="${AGE_RECIPIENT:-}"        # clé publique age (age1...)
R2_BUCKET="${R2_BUCKET:-}"                # optionnel : s3://mon-bucket/qdrant
RETENTION_DAYS="${RETENTION_DAYS:-30}"

DATE="$(date +%Y%m%d_%H%M%S)"
FINAL_ARCHIVE="qdrant_backup_${DATE}.tar.gz.age"

AUTH_HEADER=()
[ -n "$QDRANT_API_KEY" ] && AUTH_HEADER=(-H "api-key: ${QDRANT_API_KEY}")

command -v jq >/dev/null || { echo "[-] jq requis"; exit 1; }
mkdir -p "$BACKUP_DIR"

echo "[*] Demande de snapshot pour '${COLLECTION_NAME}'..."
RESPONSE=$(curl -sf -X POST "${AUTH_HEADER[@]}" \
  "http://${QDRANT_HOST}:${QDRANT_PORT}/collections/${COLLECTION_NAME}/snapshots") || {
  echo "[-] Échec de la création du snapshot (Qdrant injoignable ou collection absente)"; exit 1; }

SNAPSHOT_FILE=$(echo "$RESPONSE" | jq -r '.result.name // empty')
[ -n "$SNAPSHOT_FILE" ] || { echo "[-] Nom de snapshot introuvable : $RESPONSE"; exit 1; }
echo "[+] Snapshot en cours : $SNAPSHOT_FILE"

# Attente active du statut (au lieu d'un sleep 3 aveugle)
for _ in $(seq 1 60); do
  STATUS=$(curl -sf "${AUTH_HEADER[@]}" \
    "http://${QDRANT_HOST}:${QDRANT_PORT}/collections/${COLLECTION_NAME}/snapshots/${SNAPSHOT_FILE}" \
    -o /dev/null -w '%{http_code}' || echo "000")
  [ "$STATUS" = "200" ] && break
  sleep 2
done
[ "$STATUS" = "200" ] || { echo "[-] Snapshot jamais devenu disponible"; exit 1; }

TMP_SNAPSHOT="${BACKUP_DIR}/${SNAPSHOT_FILE}"
curl -sf "${AUTH_HEADER[@]}" -o "$TMP_SNAPSHOT" \
  "http://${QDRANT_HOST}:${QDRANT_PORT}/collections/${COLLECTION_NAME}/snapshots/${SNAPSHOT_FILE}"

# Archivage + chiffrement réel
cd "$BACKUP_DIR"
tar -czf - "$SNAPSHOT_FILE" > "qdrant_backup_${DATE}.tar.gz"
rm -f "$TMP_SNAPSHOT"

if [ -n "$AGE_RECIPIENT" ] && command -v age >/dev/null; then
  age -r "$AGE_RECIPIENT" -o "$FINAL_ARCHIVE" "qdrant_backup_${DATE}.tar.gz"
  rm -f "qdrant_backup_${DATE}.tar.gz"
  echo "[+] Archive chiffrée : ${BACKUP_DIR}/${FINAL_ARCHIVE}"
else
  FINAL_ARCHIVE="qdrant_backup_${DATE}.tar.gz"
  echo "[!] AGE_RECIPIENT non configuré : archive NON chiffrée. Configurez une clé."
fi

# Copie hors site (une sauvegarde sur le même disque n'est pas une sauvegarde)
if [ -n "$R2_BUCKET" ] && command -v rclone >/dev/null; then
  rclone copyto "${BACKUP_DIR}/${FINAL_ARCHIVE}" "${R2_BUCKET}/${FINAL_ARCHIVE}"
  echo "[+] Copie hors site OK : ${R2_BUCKET}/${FINAL_ARCHIVE}"
fi

# Rotation + alerte si l'espace disque devient critique
find "$BACKUP_DIR" -name "qdrant_backup_*.tar.gz*" -mtime "+${RETENTION_DAYS}" -delete
DISK_PCT=$(df -P "$BACKUP_DIR" | awk 'NR==2 {print $5}' | tr -d '%')
[ "${DISK_PCT:-0}" -gt 85 ] && echo "[!] ALERTE : ${DISK_PCT}% d'espace disque utilisé"

echo "[+] Sauvegarde terminée : ${FINAL_ARCHIVE}"
