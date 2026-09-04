# autonomous-ad-agent

Prototype autonome « zéro-budget » — Agent publicitaire générateur de contenu.

**But :** générer automatiquement des pages SEO/landing et déployer en site
statique sans dépenses (aucun appel LLM payant : génération heuristique).

## Contenu

- `orchestrator.py` — orchestrateur principal (génère keywords, articles, build site)
- `keywords.py` — générateur de mots-clés long-tail (offline)
- `generate_article.py` — génération d'articles via templates (heuristique)
- `build_site.py` — assembly du site statique dans `./site/`
- `templates/` — templates Jinja2 pour pages et index
- `.github/workflows/deploy.yml` — workflow GitHub Actions : exécution planifiée + déploiement gh-pages
- `requirements.txt` — dépendances Python
- `.env.example` — variables d'environnement optionnelles

## Installation & exécution locale

```bash
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # puis ajustez si besoin
python orchestrator.py            # génère ./site/ (pages + index.html)
```

Résultat : le dossier `./site/` contient le site statique prêt à déployer.

## Déploiement automatique (GitHub Pages)

Poussez ce dépôt sur GitHub. Le workflow `.github/workflows/deploy.yml`
s'exécutera automatiquement :
- sur chaque `push` vers `main`,
- selon le planificateur `cron` (par défaut tous les jours à 03:00 UTC, ajustable).

Il régénère le site puis le déploie sur la branche `gh-pages` (via
`GITHUB_TOKEN`). Pensez à activer GitHub Pages → source `gh-pages` dans les
réglages du dépôt.

## Notes

- **Zéro budget** : pas d'appels LLM payants, génération heuristique. Qualité
  acceptable pour du bootstrap SEO / volume, mais surveillez et améliorez le
  contenu (les méta-descriptions et textes restent basiques).
- `mastodon.py` est optionnel (non utilisé pour l'instant) ; supprimez-le si
  vous n'en avez pas besoin.
- Respectez les conditions d'utilisation : pas d'auto-posting abusif.
