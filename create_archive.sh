#!/usr/bin/env bash
set -euo pipefail

ROOT="autonomous-ad-agent"
rm -rf "$ROOT"
mkdir -p "$ROOT"/templates
mkdir -p "$ROOT"/.github/workflows

cat > "$ROOT/README.md" <<'EOF'
Prototype autonome "zéro-budget" — Agent publicitaire générateur de contenu
---
But : générer automatiquement des pages SEO/landing et déployer en site statique sans dépenses.

Contenu :
- orchestrator.py : orchestrateur principal (génère keywords, articles, build site)
- keywords.py : générateur de mots-clés long-tail (offline)
- generate_article.py : génération d'articles via templates (heuristique)
- build_site.py : assembly du site statique dans ./site/
- templates/ : templates Jinja2 pour pages et index
- .github/workflows/deploy.yml : workflow GitHub Actions pour exécution planifiée & déploiement gh-pages
- requirements.txt : dépendances Python

Installation & exécution locale :
1) python3 -m venv venv && source venv/bin/activate
2) pip install -r requirements.txt
3) Copier .env.example -> .env et ajuster (AFFILIATE_ID si besoin, MASTODON_* si vous voulez activer la post)
4) python orchestrator.py
   -> génère ./site/ avec pages et ./site/index.html

Déploiement automatique :
- Poussez ce repo sur GitHub. Le workflow .github/workflows/deploy.yml s'exécutera automatiquement sur push et selon la planification (cron) pour regenerer et déployer vers gh-pages (utilise GITHUB_TOKEN).

Notes :
- Zéro budget = pas d'appels LLM payants, génération heuristique. Qualité acceptable pour bootstrap SEO/volume, mais surveillez et améliorez le contenu.
- Respectez ToS, n’utilisez pas d’auto-posting abusif.
EOF

cat > "$ROOT/requirements.txt" <<'EOF'
Jinja2==3.1.2
python-dotenv==1.0.0
requests==2.31.0
mastodon.py==1.6.0
EOF

cat > "$ROOT/.env.example" <<'EOF'
# Variables options
AFFILIATE_ID=TEST_AFFIL
# Optionnel pour poster sur Mastodon si vous activez publish_posting
MASTODON_BASE_URL=https://mastodon.social
MASTODON_TOKEN=
# Nombre d'articles générés par exécution
N_PER_RUN=6
EOF

cat > "$ROOT/orchestrator.py" <<'EOF'
#!/usr/bin/env python3
"""
Orchestrateur principal : génère keywords, articles et construit le site.
Exécution : python orchestrator.py
"""
import os
from dotenv import load_dotenv
from keywords import generate_keywords
from generate_article import generate_article
from build_site import build_site

load_dotenv()

# Configuration
OUT_DIR = os.path.join(os.path.dirname(__file__), "site")
N_PER_RUN = int(os.getenv("N_PER_RUN", "6"))  # nombre d'articles à générer par run

def main():
    print("[orchestrator] génération des mots-clés...")
    seeds = ["meilleur casque audio", "outil productivité", "chaise bureau ergonomique", "sac à dos photo"]
    keywords = generate_keywords(seeds, max_out=200)
    chosen = keywords[:N_PER_RUN]
    print(f"[orchestrator] {len(chosen)} mots-clés sélectionnés pour génération :")
    for k in chosen:
        print(" -", k)

    articles = []
    for kw in chosen:
        art = generate_article(kw)
        articles.append(art)

    print("[orchestrator] construction du site statique...")
    build_site(articles, out_dir=OUT_DIR)
    print(f"[orchestrator] site généré dans {OUT_DIR}")

if __name__ == "__main__":
    main()
EOF

cat > "$ROOT/keywords.py" <<'EOF'
"""
Générateur simple de mots-clés long-tail (offline).
Ne fait pas appel à des APIs externes : combine seed phrases avec question-words et modifiers.
"""
from itertools import product

QUESTION_WORDS = ["pourquoi", "comment", "meilleur", "moins cher", "avis", "2026", "guide", "comparatif"]
MODIFIERS = ["pour débutant", "pas cher", "haut de gamme", "alternatives", "avis francais"]

def generate_keywords(seeds, max_out=100):
    """
    seeds: liste de phrases de départ
    renvoie une liste unique de mots-clés long-tail
    """
    out = []
    for s in seeds:
        s = s.strip()
        out.append(s)
        for q in QUESTION_WORDS:
            out.append(f"{s} {q}")
        for m in MODIFIERS:
            out.append(f"{s} {m}")
        # variantes courtes
        for i in range(1,4):
            out.append(f"{s} {i} avis")
    # dédupliquer en gardant l'ordre
    seen = set()
    result = []
    for k in out:
        if k not in seen:
            seen.add(k)
            result.append(k)
        if len(result) >= max_out:
            break
    return result
EOF

cat > "$ROOT/generate_article.py" <<'EOF'
"""
Génération d'un article HTML minimal depuis un keyword.
Approche heuristique/template : title, intro, pros/cons, FAQ, CTA-affiliate.
"""
import os
import re
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)

def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    s = s.replace(" ", "-")
    return s[:120]

def generate_content_paragraphs(keyword):
    # génération heuristique de paragraphes
    intro = f"Vous cherchez « {keyword} » ? Ce guide explique simplement ce qu'il faut savoir, les avantages et comment choisir."
    overview = "Résumé rapide : " + " ".join([f"Point clé sur {keyword}," for _ in range(2)])[:-1] + "."
    pros = [
        f"Bonne option pour {keyword}",
        f"Prix attractif pour l'usage courant",
        "Bonne compatibilité et robustesse"
    ]
    cons = [
        "Peut manquer de fonctionnalités avancées",
        "Qualité variable selon le modèle",
    ]
    faqs = [
        {"q": f"Quel est le meilleur {keyword} en 2026 ?", "a": "Cela dépend du budget et de l'usage ; privilégiez les tests et avis."},
        {"q": f"Comment choisir un {keyword} ?", "a": "Vérifiez les critères essentiels : confort, durabilité, garanties."}
    ]
    return {
        "intro": intro,
        "overview": overview,
        "pros": pros,
        "cons": cons,
        "faqs": faqs
    }

def generate_article(keyword, affiliate_id_env="AFFILIATE_ID"):
    """
    Retourne un dict article:
    {
      'title', 'slug', 'html', 'meta_description', 'affiliate_link'
    }
    """
    tpl = env.get_template("article.html.jinja")
    q = keyword.strip()
    slug = slugify(q)
    parts = generate_content_paragraphs(q)
    affiliate_id = os.getenv(affiliate_id_env, "AFFILIATE_PLACEHOLDER")
    # exemple de lien d'affiliation générique (à remplacer par votre systeme)
    affiliate_link = f"https://example.com/aff?product={slug}&aff={affiliate_id}"
    html = tpl.render(title=q, keyword=q, intro=parts["intro"], overview=parts["overview"],
                      pros=parts["pros"], cons=parts["cons"], faqs=parts["faqs"],
                      affiliate_link=affiliate_link)
    return {
        "title": q,
        "slug": slug,
        "html": html,
        "meta_description": parts["overview"],
        "affiliate_link": affiliate_link
    }
EOF

cat > "$ROOT/build_site.py" <<'EOF'
"""
Assemble les pages dans out_dir (dossier ./site).
Crée index.html et une page par article.
"""
import os
import shutil
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def build_site(articles, out_dir="site"):
    # nettoyer dossier
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    ensure_dir(out_dir)
    # assets minimal
    ensure_dir(os.path.join(out_dir, "assets"))
    # écrire pages articles
    for a in articles:
        path = os.path.join(out_dir, f"{a['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(a["html"])
    # index
    tpl = env.get_template("index.html.jinja")
    index_html = tpl.render(articles=articles)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
EOF

cat > "$ROOT/templates/article.html.jinja" <<'EOF'
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{{ title }} — Guide rapide</title>
  <meta name="description" content="{{ meta_description | default('Guide et comparatif') }}">
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color:#111 }
    header h1 { font-size: 1.6rem; }
    .cta { background:#0b74de; color:#fff; padding:.8rem; display:inline-block; margin:1rem 0; text-decoration:none; border-radius:6px }
    .box { border:1px solid #eee; padding:1rem; border-radius:6px; margin:1rem 0; background:#fbfbfb }
  </style>
</head>
<body>
  <header>
    <h1>{{ title }}</h1>
    <p><em>{{ intro }}</em></p>
  </header>

  <section class="box">
    <h2>Résumé</h2>
    <p>{{ overview }}</p>
  </section>

  <section>
    <h3>Avantages</h3>
    <ul>
      {% for p in pros %}
      <li>{{ p }}</li>
      {% endfor %}
    </ul>
    <h3>Inconvénients</h3>
    <ul>
      {% for c in cons %}
      <li>{{ c }}</li>
      {% endfor %}
    </ul>
  </section>

  <section>
    <a class="cta" href="{{ affiliate_link }}" rel="nofollow noopener" target="_blank">Voir le produit recommandé</a>
  </section>

  <section>
    <h3>FAQ</h3>
    {% for f in faqs %}
      <p><strong>{{ f.q }}</strong><br/>{{ f.a }}</p>
    {% endfor %}
  </section>

  <footer>
    <p>Article généré automatiquement — liens d'affiliation inclus.</p>
  </footer>
</body>
</html>
EOF

cat > "$ROOT/templates/index.html.jinja" <<'EOF'
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Site généré — index</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; color:#111 }
    a { color:#0b74de; text-decoration:none }
    li { margin: .6rem 0 }
  </style>
</head>
<body>
  <header>
    <h1>Articles récents</h1>
    <p>Site généré automatiquement — version prototype.</p>
  </header>
  <main>
    <ul>
      {% for a in articles %}
        <li><a href="{{ a.slug }}.html">{{ a.title }}</a> — <small>{{ a.meta_description }}</small></li>
      {% endfor %}
    </ul>
  </main>
  <footer>
    <p>Généré par l'agent autonome prototype.</p>
  </footer>
</body>
</html>
EOF

cat > "$ROOT/.github/workflows/deploy.yml" <<'EOF'
name: Génération & Déploiement automatique

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 3 * * *'  # quotidien à 03:00 UTC (ajustable)

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run orchestrator
        run: |
          python orchestrator.py

      - name: Deploy to GitHub Pages (gh-pages branch)
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
EOF

echo "Création de l'archive zip autonomous-ad-agent.zip ..."
zip -r autonomous-ad-agent.zip "$ROOT" >/dev/null

echo "Archive créée : autonomous-ad-agent.zip"
echo "Contenu du dossier $ROOT :"
find "$ROOT" -maxdepth 2 -print
echo
echo "Pour extraire : unzip autonomous-ad-agent.zip"
EOF

Instructions d'utilisation (rapide)
- Enregistrez le script ci‑dessus dans create_archive.sh, puis exécutez :
  - chmod +x create_archive.sh
  - ./create_archive.sh
- Résultat : autonomous-ad-agent.zip dans le même dossier. Dézippez-le puis vous pouvez :
  - l’examiner localement,
  - le pousser dans un repo GitHub (git init && git add . && git commit && git remote add origin ... && git push -u origin main),
  - ou déployer manuellement les fichiers.

Souhaitez‑vous que je vous fournisse aussi la commande git exacte pour initialiser et pousser le repo après extraction (avec exemples) ?