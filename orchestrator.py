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
