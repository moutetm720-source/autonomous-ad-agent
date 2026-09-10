#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparateur : coût FIXE (serveur GPU) vs coût VARIABLE (API de tokens).

Répond à une seule question : à partir de combien de tokens par mois
un GPU 24/7 devient-il moins cher qu'une API hébergée dans l'UE ?

Usage :
    python3 outils/calcul_couts.py
    python3 outils/calcul_couts.py --ratio 0.8 --heures 40   # 40 h/mois d'utilisation réelle
"""

import argparse

USD_EUR = 0.92  # taux de conversion indicatif, à ajuster

# ----------------------------------------------------------------------------
# 1. Coût FIXE : location GPU en France (prix publics constatés, 2026)
#    L4 24 Go ~ 0,75-0,91 EUR/h ; L40S 48 Go ~ 1,40-1,70 EUR/h ; H100 ~ 3 EUR/h
# ----------------------------------------------------------------------------
GPU = {
    "L4 24 Go (Scaleway)": 0.85,
    "L40S 48 Go (Scaleway)": 1.50,
    "H100 80 Go (Scaleway/OVH)": 3.00,
}

# Ce que chaque carte peut réellement héberger (2026) :
GPU_PEUT_CHARGER = {
    "L4 24 Go (Scaleway)": "Qwen 3.6 27B (~17 Go VRAM) -> correct, pas frontière",
    "L40S 48 Go (Scaleway)": "Qwen3-Coder 80B-A3B (~48 Go) -> ~96% du frontière",
    "H100 80 Go (Scaleway/OVH)": "Devstral-2 123B / GLM quantifié -> quasi frontière",
}

# ----------------------------------------------------------------------------
# 2. Coût VARIABLE : API open-weights hébergées dans l'UE (USD / million tokens)
# ----------------------------------------------------------------------------
API = {
    # Scaleway Sovereign AI (France) : pas de collecte/réutilisation des prompts
    "Scaleway qwen3.6-35b-a3b": (0.29, 1.73),
    "Scaleway gpt-oss-120b": (0.17, 0.69),
    "Scaleway mistral-small-3.2-24b": (0.17, 0.40),
    "Scaleway glm-5.2 (frontière)": (2.08, 6.34),
    # Mistral La Plateforme (France)
    "Mistral Codestral": (0.30, 0.90),
    "Mistral Large 3": (0.50, 1.50),
}

# Profils de consommation mensuelle (tokens) d'une agence 1-2 personnes
PROFILS = {
    "Bootstrapping (1 app/mois, ~5 M tokens)": 5,
    "1 client actif (~20 M tokens)": 20,
    "3 clients actifs (~60 M tokens)": 60,
    "Usine à plein régime (~200 M tokens)": 200,
    "Volume industriel (~600 M tokens)": 600,
}

PROFILS_GPU = {
    "Bootstrapping (1 app/mois, ~5 M tokens)": "L4 24 Go (Scaleway)",
    "1 client actif (~20 M tokens)": "L4 24 Go (Scaleway)",
    "3 clients actifs (~60 M tokens)": "L40S 48 Go (Scaleway)",
    "Usine à plein régime (~200 M tokens)": "H100 80 Go (Scaleway/OVH)",
    "Volume industriel (~600 M tokens)": "H100 80 Go (Scaleway/OVH)",
}


def prix_mixte(in_usd: float, out_usd: float, ratio_in: float) -> float:
    """Prix moyen d'un million de tokens, en EUR, pour un ratio entrée/sortie donné."""
    return (ratio_in * in_usd + (1 - ratio_in) * out_usd) * USD_EUR


def euros(x: float) -> str:
    return f"{x:,.2f} €".replace(",", " ")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ratio", type=float, default=0.75,
                   help="part des tokens en entrée (contexte + RAG), défaut 0.75")
    p.add_argument("--heures", type=int, default=730,
                   help="heures/mois de location GPU (730 = 24/7)")
    p.add_argument("--usage-reel", type=int, default=0,
                   help="heures/mois d'utilisation RÉELLE du GPU (0 = on paie 24/7)")
    args = p.parse_args()

    print("=" * 96)
    print("COÛT FIXE (GPU loué à l'année) — combien ça coûte, même à ne rien faire")
    print("=" * 96)
    print(f"{'Carte':<34}{'€/h':>8}{'24/7 (730 h)':>16}{'Modèle réellement chargeable'}")
    print("-" * 96)
    gpu_mensuel = {}
    for carte, prix_h in GPU.items():
        m = prix_h * args.heures
        gpu_mensuel[carte] = m
        print(f"{carte:<34}{prix_h:>8.2f}{euros(m):>16}   {GPU_PEUT_CHARGER[carte]}")
    print()
    print("À comparer avec un poste de travail d'occasion (RTX 3090 24 Go ~ 700 €) :")
    print("  amorti sur 24 mois = ~29 €/mois + ~25 €/mois d'électricité = ~55 €/mois, chez vous.")

    print()
    print("=" * 96)
    print("COÛT VARIABLE (API souveraine) — on ne paie que ce qu'on consomme")
    print("=" * 96)
    print(f"{'Modèle':<34}{'entrée $/M':>12}{'sortie $/M':>12}{'mixte €/M':>12}")
    print("-" * 96)
    mixte = {}
    for modele, (i, o) in API.items():
        pm = prix_mixte(i, o, args.ratio)
        mixte[modele] = pm
        print(f"{modele:<34}{i:>12.2f}{o:>12.2f}{euros(pm):>12}")
    print(f"\n(ratio entrée/sortie = {args.ratio:.0%} / {1-args.ratio:.0%})")

    print()
    print("=" * 96)
    print(f"SEUIL DE RENTABILITÉ — volume mensuel à partir duquel le GPU gagne")
    print("=" * 96)
    print(f"{'Carte':<34}" + "".join(f"{m.split()[0]:>13}" for m in API) + "   (en millions de tokens/mois)")
    print("-" * 96)
    for carte, m in gpu_mensuel.items():
        ligne = f"{carte:<34}"
        for modele in API:
            ligne += f"{m / mixte[modele]:>13,.0f}"
        print(ligne)
    print()
    print("Lecture : avec un Qwen 35B sur Scaleway, il faut consommer ~1 000 millions de tokens")
    print("par mois (soit ~200 applications complètes/mois) pour qu'un L4 24/7 soit rentable.")

    print()
    print("=" * 96)
    print("PAR PROFIL D'ACTIVITÉ — ce que vous payez réellement")
    print("=" * 96)
    print(f"{'Profil':<44}{'GPU 24/7':>13}{'API (médiane)':>16}{'Gagnant':>12}")
    print("-" * 96)
    couts_api = sorted(mixte.values())
    mediane_api = (couts_api[len(couts_api) // 2 - 1] + couts_api[len(couts_api) // 2]) / 2
    for profil, millions in PROFILS.items():
        carte = PROFILS_GPU[profil]
        c_gpu = gpu_mensuel[carte]
        c_api = millions * mediane_api
        gagnant = "API" if c_api < c_gpu else "GPU"
        print(f"{profil:<44}{euros(c_gpu):>13}{euros(c_api):>16}{gagnant:>12}  (vs {carte.split(' (')[0]})")

    print()
    print(f"Prix médian constaté des API open-weights UE : {euros(mediane_api)} / million de tokens")
    print("=> Une app Flutter complète (~5 M tokens d'allers-retours agents) revient à "
          f"{euros(5 * mediane_api)} de tokens.")

    if args.usage_reel:
        print()
        print("=" * 96)
        print(f"ET SI ON NE LOUAIT LE GPU QUE PENDANT LES {args.usage_reel} h D'USAGE RÉEL ?")
        print("=" * 96)
        for carte, prix_h in GPU.items():
            m = prix_h * args.usage_reel
            print(f"{carte:<34} {euros(m):>12} / mois  "
                  f"(au lieu de {euros(gpu_mensuel[carte])})  "
                  f"=> {gpu_mensuel[carte]/m:.1f}× moins cher")
        print("\nUn GPU à l'usage = on l'allume, on génère, on l'éteint. C'est 10 à 20× moins cher")
        print("que le 24/7, et c'est la seule façon rationnelle de démarrer sur du self-hosté.")

    print()
    print("=" * 96)
    print("COÛT DE REVIENT D'UNE APPLICATION (hors temps humain)")
    print("=" * 96)
    for nom, (i, o) in API.items():
        pm = prix_mixte(i, o, args.ratio)
        print(f"{nom:<34} ~{euros(5 * pm):>9} de tokens pour 5 M tokens (1 app complète)")
    print("\nHébergement client (PaaS FR type Scalingo/Clever Cloud) : 6 à 20 €/mois, refacturé")
    print("30 à 60 €/mois dans le contrat de maintenance. C'est de la marge, pas une charge.")


if __name__ == "__main__":
    main()
