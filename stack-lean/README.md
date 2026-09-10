# Stack lean — agence IA sans GPU

Équivalent allégé et corrigé du `docker-compose.yml` du plan initial.
**Coût de fonctionnement : 0 € de fixe.** Tourne sur votre machine ou sur un VPS à 5 €.

## Ce qui a changé

| Plan initial | Ici | Pourquoi |
|---|---|---|
| vLLM + GPU dédié | **LiteLLM → Scaleway / Mistral (UE)** | 620 €/mois → 0 € de fixe |
| DeepSeek-Coder-V2 (2024) | **Frontière 2026 à la demande** | Le L4 ne pouvait pas charger les modèles récents |
| Langflow (port 7860 public) | **Scripts Python versionnés** | RCE non authentifiée CVSS 9.8 (CVE-2025-3248) ; et ce qui n'est pas dans Git est perdu |
| Qdrant sans clé, exposé | **Clé API + aucun port publié** | Art. 32 RGPD |
| Pas d'embedding | **`multilingual-e5-large` via LiteLLM** | Sans lui, le RAG ne peut pas fonctionner |
| 5 ports publics | **1 seul, derrière Caddy + auth** | Surface d'attaque divisée par 5 |
| Sauvegarde « chiffrée » non chiffrée | **`age` + copie S3/R2 + attente active** | Le script d'origine ne créait même pas le snapshot |

## Démarrage

```bash
cd stack-lean

# 1. Secrets
cp .env.example .env
#    Remplir SCALEWAY_API_KEY et/ou MISTRAL_API_KEY.
#    Générer les trois clés internes :
for k in LITELLM_MASTER_KEY QDRANT_API_KEY WEBUI_SECRET_KEY; do
  echo "$k=$(openssl rand -hex 32)" >>.env
done
#    Mot de passe du portail :
docker run --rm caddy:2 caddy hash-password      # coller le hash dans CADDY_PASSWORD_HASH

# 2. Démarrer
docker compose up -d

# 3. Initialiser la mémoire vectorielle (dimension détectée automatiquement)
pip install requests python-dotenv
python3 init_qdrant.py
```

Interface : `http://localhost:8080`. LiteLLM : `http://localhost:8080/v1`.

## Modèles disponibles (via LiteLLM)

| Alias | Modèle réel | Usage |
|---|---|---|
| `agence/rapide` | Scaleway `qwen3.6-35b-a3b` | Travail courant, ~0,60 €/M tokens |
| `agence/rapide-alt` | Mistral `codestral-latest` | Repli, spécialiste code 256K |
| `agence/expert` | Scaleway `glm-5.2` | Architecture, bugs durs, ~2,89 €/M |
| `scaleway/multilingual-e5-large` | embeddings | RAG (indispensable) |
| `agence/brouillon` | Ollama local `qwen2.5-coder:7b` | Brouillons, coût marginal nul |

Changer de fournisseur = modifier `litellm_config.yaml`. **Le code des agents ne bouge pas.**

## Garde-fou budgétaire

`litellm_config.yaml` fixe `max_budget: 120` € / 30 jours. Au-delà, LiteLLM refuse les
appels au lieu de laisser filer la facture. À ajuster quand l'activité le justifie — c'est
votre seule protection contre une boucle d'agent qui s'emballe.

## Activer le local plus tard (optionnel)

```bash
docker compose --profile local up -d
docker compose exec ollama ollama pull qwen2.5-coder:7b-instruct-q5_K_M
```

Un petit modèle local absorbe les brouillons, le formatage et les embeddings : **~80 % des
appels**, donc ~80 % de la facture de tokens en moins. C'est le meilleur rapport
investissement/économie avant tout achat de GPU.

## Sauvegarde

```bash
export AGE_RECIPIENT=age1...        # clé publique, à conserver HORS du serveur
export R2_BUCKET=s3://mon-bucket/qdrant
./backup_qdrant.sh                  # en cron, une fois par nuit
```

Sans `AGE_RECIPIENT`, le script prévient que l'archive n'est **pas** chiffrée et continue —
mieux vaut une sauvegarde nue qu'aucune sauvegarde, mais configurez la clé.
