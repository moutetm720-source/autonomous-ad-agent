#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Remplace (gratuitement et de façon déterministe) l'« agent QA » du plan :
# interdit les secrets codés en dur avant chaque commit / chaque build.
# À lancer en pré-commit et dans la CI. Ne nécessite AUCUN GPU, AUCUN LLM.
# ---------------------------------------------------------------------------
set -euo pipefail

echo "[qa] scan des secrets codés en dur..."

# 1. Motifs de secrets évidents dans le code Dart / Dart-defines
PATTERNS=(
  'sk-[A-Za-z0-9]{20,}'                # OpenAI / compatibles
  'AIza[0-9A-Za-z_-]{35}'              # Google / Firebase / Maps
  'xox[baprs]-[A-Za-z0-9-]{10,}'       # Slack
  'ghp_[A-Za-z0-9]{36}'                # GitHub PAT
  'glpat-[A-Za-z0-9_-]{20,}'           # GitLab
  'AKIA[0-9A-Z]{16}'                   # AWS
  'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.'  # JWT
  '-----BEGIN [A-Z ]*PRIVATE KEY-----' # clé privée
)

# Fichiers concernés (hors générés, hors tests de fixtures)
FILES=$(git ls-files '*.dart' '*.yaml' '*.yml' '*.json' '*.env*' 2>/dev/null || \
        find . -name '*.dart' -not -path './.git/*')

FOUND=0
for pat in "${PATTERNS[@]}"; do
  if echo "$FILES" | xargs grep -InE "$pat" 2>/dev/null; then
    FOUND=1
  fi
done
[ "$FOUND" -eq 0 ] || { echo "[qa] ÉCHEC : secret potentiel détecté (voir ci-dessus)."; exit 1; }

# 2. Toute clé doit venir de flutter_dotenv / --dart-define, jamais d'un littéral
if echo "$FILES" | xargs grep -InE '(apiKey|api_key|secret|token|password)\s*[:=]\s*"[A-Za-z0-9_\-]{16,}"' 2>/dev/null; then
  echo "[qa] ÉCHEC : clé écrite en dur. Utilisez String.fromEnvironment() ou dotenv.env['...']."
  exit 1
fi

# 3. Le .env ne doit jamais être versionné
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  echo "[qa] ÉCHEC : .env est versionné. Ajoutez-le à .gitignore et purgez l'historique."
  exit 1
fi

# 4. Les platforms natives ne doivent pas embarquer de clé
for f in android/app/google-services.json ios/Runner/GoogleService-Info.plist; do
  if [ -f "$f" ] && git ls-files --error-unmatch "$f" >/dev/null 2>&1; then
    echo "[qa] ATTENTION : $f versionné. Vérifiez qu'il ne contient pas de secret exploitable."
  fi
done

echo "[qa] OK : aucun secret détecté."
