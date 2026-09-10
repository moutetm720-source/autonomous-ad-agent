# autonomous-ad-agent

Prototype « zéro budget » d'agent autonome générant des pages SEO et les déployant en site
statique (GitHub Actions + GitHub Pages), **et** base de travail d'un projet d'agence de
développement d'applications (Flutter) pour PME, associations et mairies.

## Contenu du dépôt

| Dossier | Rôle |
|---|---|
| `orchestrator.py`, `keywords.py`, `generate_article.py`, `build_site.py`, `templates/` | Le prototype d'agent publicitaire d'origine. Réutilisé tel quel pour **l'acquisition à coût nul** de l'agence (voir `docs/02-plan-lean.md` § « Acquisition »). |
| `create_archive.sh` | Régénère l'archive autoportante du prototype. |
| `docs/01-analyse-critique.md` | **Analyse chiffrée du plan d'agence IA** : coûts, risques, bugs des scripts fournis. |
| `docs/02-plan-lean.md` | Le plan d'exécution en 4 phases, de 0 € au premier client récurrent. |
| `docs/03-grille-tarifaire.md` | Grille tarifaire, contrat de maintenance, seuils de marché public. |
| `outils/calcul_couts.py` | Calculateur GPU 24/7 vs API au token : reproduit tous les chiffres du doc 01. |
| `stack-lean/` | `docker-compose.yml` corrigé et sans GPU : LiteLLM, Qdrant sécurisé, Open WebUI, Caddy. |
| `stack-lean/init_qdrant.py` | Version corrigée : dimension d'embedding **détectée**, plus jamais devinée. |
| `stack-lean/backup_qdrant.sh` | Version corrigée : le `$` manquant est réparé, chiffrement réel (`age`), copie hors site. |
| `scripts/check_secrets.sh` | Contrôle déterministe des secrets codés en dur — remplace l'« agent QA » par 40 lignes de shell. |
| `ci/quality-gate.yml` | Pipeline qualité/sécurité Flutter gratuite et reproductible. |
| `agents/` | Les trois prompts d'agents, réécrits pour **réutiliser le socle** avant de créer. |

## Démarrer

```bash
# 1. Comprendre le coût réel de l'infrastructure
python3 outils/calcul_couts.py
python3 outils/calcul_couts.py --usage-reel 40     # variante GPU allumé à la demande

# 2. Lancer la stack (aucun GPU requis)
cd stack-lean && cp .env.example .env && docker compose up -d

# 3. Prototype d'acquisition (site statique)
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
python3 orchestrator.py   # génère ./site/
```

## Le résultat en un coup d'œil

| | Plan initial | Plan lean |
|---|---|---|
| Dépense avant le premier client | 700 – 2 400 € | **~135 €** |
| Coût IA par application livrée | 620 €+ | **1 – 15 €** |
| Modèle | DeepSeek-Coder-V2 (2024) | Frontière 2026 à la demande |
| RAG | Inopérant (aucun embedding) | Fonctionnel |
| Exposition réseau | 5 ports publics, 2 failles critiques | 1 port, authentifié |
| Bascule vers le matériel | Jour 1 | **~10 clients récurrents** |

Voir `docs/01-analyse-critique.md` pour le détail et les sources.
