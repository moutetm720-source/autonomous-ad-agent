#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulateur de trésorerie — agence d'applications en micro-entreprise (barèmes 2026).

Répond à trois questions :
  1. Combien me reste-t-il vraiment sur 100 € encaissés ?
  2. Combien de clients récurrents me faut-il pour vivre ?
  3. À partir de quand la TVA et le plafond micro vont-ils me concerner ?

Barèmes 2026 :
  - Cotisations sociales BNC (professions libérales non réglementées, dont développeur) : 25,6 %
    (décret n° 2025-943 du 8 septembre 2025 ; 24,6 % en 2025)
  - Cotisations BIC prestations de services : 21,2 %
  - ACRE : exonération de 50 % avant le 1er juillet 2026, de 25 % à partir de cette date
  - CFP (contribution formation professionnelle) : 0,2 % en prestation de services / BNC
  - Versement libératoire de l'IR : 2,2 % (BNC) — optionnel
  - Plafond de CA micro-entreprise : 83 600 € (prestations de services, 2026-2028)
  - Franchise de TVA : 37 500 € (seuil de base) / 41 250 € (seuil majoré)

Usage :
    python3 outils/simulateur_tresorerie.py
    python3 outils/simulateur_tresorerie.py --clients 10 --forfait 189 --apps 6 --prix-app 3900
    python3 outils/simulateur_tresorerie.py --bic            # si activité déclarée en BIC
"""

import argparse

# --- Barèmes 2026 ------------------------------------------------------------
TAUX_SOCIAL_BNC = 0.256      # développeur = profession libérale non réglementée
TAUX_SOCIAL_BIC = 0.212      # prestation de services commerciale/artisanale
TAUX_ACRE_2026 = 0.75        # à partir du 01/07/2026 : on paie 75 % du taux normal
TAUX_CFP = 0.002             # contribution à la formation professionnelle
TAUX_VERSEMENT_LIB = 0.022   # optionnel, BNC
PLAFOND_MICRO = 83_600       # prestations de services, 2026-2028
SEUIL_TVA_BASE = 37_500      # franchise de TVA, prestations de services
TVA = 0.20

# --- Charges professionnelles annuelles (estimations à ajuster) ---------------
CFE = 300           # cotisation foncière des entreprises (base minimum, variable par commune)
RC_PRO = 320        # responsabilité civile professionnelle, développeur/prestataire informatique
COMPTABLE = 0       # 0 en micro sans comptable ; ~600-900 € si accompagnement
OUTILS_MENSUEL = 30 # dépôt privé, domaines, comptes développeurs (Apple/Play lissés)


def eur(x):
    return f"{x:,.0f} €".replace(",", " ")


def simuler(clients, forfait, apps, prix_app, bic=False, versement_lib=True,
            cout_direct_client=20, tokens_mensuel=25):
    taux_social = TAUX_SOCIAL_BIC if bic else TAUX_SOCIAL_BNC
    taux_annee1 = taux_social * TAUX_ACRE_2026   # ACRE réduite à 25 % d'exonération

    ca_apps = apps * prix_app
    ca_recurrent = clients * forfait * 12
    ca_total = ca_apps + ca_recurrent

    # Charges proportionnelles au CA
    cotisations_1 = ca_total * taux_annee1
    cotisations_2 = ca_total * taux_social
    cfp = ca_total * TAUX_CFP
    ir_lib = ca_total * TAUX_VERSEMENT_LIB if versement_lib else 0

    # Charges fixes
    hebergement = clients * cout_direct_client * 12
    tokens = tokens_mensuel * 12
    fixes = CFE + RC_PRO + COMPTABLE + OUTILS_MENSUEL * 12 + hebergement + tokens

    net_1 = ca_total - cotisations_1 - cfp - ir_lib - fixes
    net_2 = ca_total - cotisations_2 - cfp - ir_lib - fixes

    return dict(
        ca_apps=ca_apps, ca_recurrent=ca_recurrent, ca_total=ca_total,
        taux_social=taux_social, taux_annee1=taux_annee1,
        cotisations_1=cotisations_1, cotisations_2=cotisations_2,
        cfp=cfp, ir_lib=ir_lib, fixes=fixes,
        hebergement=hebergement, tokens=tokens,
        net_1=net_1, net_2=net_2,
    )


def afficher(titre, r):
    print("=" * 78)
    print(titre)
    print("=" * 78)
    print(f"  CA création  : {eur(r['ca_apps'])}")
    print(f"  CA récurrent : {eur(r['ca_recurrent'])}   ({r['ca_recurrent']/max(r['ca_total'],1):.0%} du CA total)")
    print(f"  CA TOTAL     : {eur(r['ca_total'])}")
    print()
    print("  Charges :")
    print(f"    cotisations sociales ({r['taux_annee1']:.2%} avec ACRE, an 1) : {eur(r['cotisations_1'])}")
    print(f"    cotisations sociales ({r['taux_social']:.2%} régime plein)      : {eur(r['cotisations_2'])}")
    print(f"    CFP 0,2 %                            : {eur(r['cfp'])}")
    print(f"    versement libératoire IR 2,2 %        : {eur(r['ir_lib'])}")
    print(f"    hébergement clients (20 €/mois)       : {eur(r['hebergement'])}")
    print(f"    tokens IA (25 €/mois)                 : {eur(r['tokens'])}")
    print(f"    fixes (CFE, RC pro, outils)           : {eur(r['fixes'] - r['hebergement'] - r['tokens'])}")
    print()
    print(f"  >>> NET AN 1 (avec ACRE) : {eur(r['net_1'])}  soit {eur(r['net_1']/12)}/mois")
    print(f"  >>> NET AN 2+ (plein)    : {eur(r['net_2'])}  soit {eur(r['net_2']/12)}/mois")
    print(f"  >>> Ce qui reste sur 100 € encaissés (an 2) : {r['net_2']/max(r['ca_total'],1)*100:.0f} €")
    print()

    if r['ca_total'] > SEUIL_TVA_BASE:
        print(f"  ⚠ TVA : CA > {eur(SEUIL_TVA_BASE)} → assujetti. Vous facturez HT + 20 % ;")
        print("    aucun impact de marge sur des clients professionnels (TVA récupérable).")
    else:
        marge_tva = SEUIL_TVA_BASE - r['ca_total']
        print(f"  ✓ TVA : encore {eur(marge_tva)} de marge avant assujettissement (franchise).")
    if r['ca_total'] > PLAFOND_MICRO:
        print(f"  ⚠ PLAFOND MICRO dépassé ({eur(PLAFOND_MICRO)}) → bascule en entreprise individuelle")
        print("    au réel, voire en société (EURL/SASU). Bon problème : le prévoir à temps.")
    else:
        print(f"  ✓ Plafond micro : {eur(PLAFOND_MICRO - r['ca_total'])} de marge restante.")
    print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--clients", type=int, default=6, help="clients sous contrat de maintenance")
    p.add_argument("--forfait", type=int, default=189, help="forfait de maintenance mensuel HT")
    p.add_argument("--apps", type=int, default=4, help="applications vendues dans l'année")
    p.add_argument("--prix-app", type=int, default=3900, help="prix de vente d'une application HT")
    p.add_argument("--bic", action="store_true", help="activité déclarée en BIC (21,2 %)")
    p.add_argument("--sans-versement-lib", action="store_true", help="pas de versement libératoire")
    args = p.parse_args()

    print()
    print("SIMULATEUR DE TRÉSORERIE — micro-entreprise, barèmes 2026")
    print("Régime :", "BIC prestations de services (21,2 %)" if args.bic else "BNC profession libérale (25,6 %)")
    print()

    scen = [
        ("A. Démarrage prudent — 3 clients, 2 apps", 3, 189, 2, 3900),
        ("B. Objectif 12 mois — 8 clients, 5 apps", 8, 189, 5, 3900),
        ("C. Régime établi — 20 clients, 10 apps", 20, 189, 10, 3900),
        ("D. Votre saisie", args.clients, args.forfait, args.apps, args.prix_app),
    ]

    for titre, c, f, a, pa in scen:
        r = simuler(c, f, a, pa, bic=args.bic, versement_lib=not args.sans_versement_lib)
        afficher(f"{titre}  [{c} clients × {f} €/mois + {a} apps × {pa} €]", r)

    print("=" * 78)
    print("RÉPONSES COURTES")
    print("=" * 78)
    print("1. Charges totales en micro-BNC (plein régime) : 25,6 + 0,2 + 2,2 = 28 % du CA.")
    print("   → sur 100 € encaissés, il reste ~72 € avant frais professionnels et IR.")
    print()
    print("2. Seuil de survie (charges perso + pro = 2 000 €/mois nets) :")
    for f in (89, 189, 389):
        # net mensuel par contrat après charges proportionnelles
        net_par_contrat = f * (1 - TAUX_SOCIAL_BNC - TAUX_CFP - TAUX_VERSEMENT_LIB)
        # coût direct du client : 20 €/mois d'hébergement
        contribution = net_par_contrat - 20
        fixes_mensuels = (CFE + RC_PRO + COMPTABLE) / 12 + OUTILS_MENSUEL + 25
        besoin = (2000 + fixes_mensuels) / contribution
        print(f"   forfait {f} €/mois → {net_par_contrat:.0f} € nets de charges, "
              f"- 20 € d'hébergement = {contribution:.0f} € de contribution")
        print(f"      → {besoin:.1f} contrats nécessaires (soit {int(besoin)+1} clients)")
    print()
    print("3. Effet de levier du récurrent : chaque contrat signé est du CA qui revient")
    print("   l'année suivante sans aucun effort commercial. 20 contrats × 189 € =")
    print(f"   {eur(20*189*12)}/an, soit l'équivalent de {20*189*12/3900:.0f} applications vendues.")
    print()
    print("Rappel : ces montants sont HT. Les taux sont ceux de 2026 ; revérifiez chaque")
    print("janvier sur autoentrepreneur.urssaf.fr. Ce script n'est pas un conseil fiscal :")
    print("faites valider votre situation par un expert-comptable.")


if __name__ == "__main__":
    main()
