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
