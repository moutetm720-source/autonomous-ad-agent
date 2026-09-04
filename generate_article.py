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
