# Grille tarifaire et contrat de maintenance récurrent

Ce document répond à la seconde option de votre plan. Il est volontairement traité **avant**
tout investissement matériel : la tarification finance l'infrastructure, pas l'inverse.

> ⚠️ Les montants sont des propositions de positionnement à valider selon votre marché local
> (Occitanie, communes de 500 à 15 000 habitants). Ils sont exprimés **HT**.

---

## 1. Règle structurante : rester sous le seuil de dispense de marché public

C'est l'information la plus rentable de ce document.

Le **décret n° 2025-1386 du 29 décembre 2025** a relevé, à compter du **1ᵉʳ avril 2026**, le
seuil de dispense de publicité et de mise en concurrence de **40 000 € HT à 60 000 € HT**
pour les marchés de fournitures et de services (art. R. 2122-8 du Code de la commande
publique) [marche-public.fr](https://www.marche-public.fr/contrats-publics/Decret-2025-1386-1383-simplification-seuils.htm) /
[Landot & Associés](https://blog.landot-avocats.net/2026/04/01/marches-publics-relevement-du-seuil-de-dispense-de-procedure-a-60-000-e-des-aujourdhui/).

**Traduction commerciale :** une mairie peut vous commander directement, sur simple devis,
sans publicité ni mise en concurrence, si la valeur estimée du besoin reste **inférieure à
60 000 € HT** — en incluant toutes les reconductions.

D'où deux conséquences immédiates sur votre grille :

1. **Chaque offre est calibrée pour rester très en dessous de 60 000 € HT sur 36 mois.**
   Exemple : mairie à 3 900 € + 389 €/mois sur 36 mois = **17 904 € HT**, soit 3,4× sous le
   seuil. Le maire signe en quinze jours au lieu de lancer une consultation de six mois.
2. **Argument de vente explicite à utiliser en rendez-vous** : « votre projet reste sous le
   seuil des 60 000 €, vous pouvez donc nous confier le marché directement, sans procédure. »
   Vous supprimez la principale objection — la peur de l'appel d'offres — avant qu'elle
   n'apparaisse.

Le même décret abaisse par ailleurs de 2× à 1,5× le plafond de chiffre d'affaires exigible,
ce qui facilite l'accès des TPE à la commande publique.

---

## 2. Création (paiement unique)

### Pack Mairie

| Prestation | Contenu | Prix HT |
|---|---|---|
| **Signalement citoyen** (socle) | App PWA + Android, photo + géolocalisation, back-office de traitement, notification de prise en charge, registre RGPD | **3 900 €** |
| Module *Cantine scolaire* | inscriptions, réservations, absences, facturation simple | + 1 900 € |
| Module *Alertes* (travaux, météo, événements) | push ciblées par zone, programmation | + 1 200 € |
| Module *Annuaire local* | associations, commerces, artisans, recherche | + 1 400 € |
| Module *Agenda / réservation de salles* | disponibilités, demandes, validation | + 900 € |
| Étude d'impact RGPD (AIPD) | obligatoire en pratique dès signalement géolocalisé de personnes | + 750 € |
| Publication iOS (App Store) | dont compte Apple 99 €/an refacturé | + 600 € |
| **Pack complet mairie** | socle + cantine + annuaire + alertes + AIPD | **8 500 €** |

### Pack PME / Commerce / Restauration

| Prestation | Contenu | Prix HT |
|---|---|---|
| **Click & Collect** | catalogue, panier, créneaux, paiement, notifications | **2 900 €** |
| Module *Prise de rendez-vous* | agenda, rappels, anti-doublon | + 1 500 € |
| Module *Fidélité & campagnes push* | carte dématérialisée, segmentation, offres | + 1 500 € |
| Module *Paiement en ligne* | Stripe / SumUp, avoirs, remboursements | + 900 € |
| **Pack commerce complet** | les quatre | **5 900 €** |

### Pack Association

| Prestation | Contenu | Prix HT |
|---|---|---|
| **Adhésions & cotisations** | formulaire, paiement, reçus fiscaux, relances | **2 400 €** |
| Module *Dons & cagnottes* | paiement récurrent, reçus automatiques | + 1 200 € |
| Module *Calendrier & inscriptions* | événements, jauges, liste d'émargement | + 900 € |
| **Pack association complet** | les trois | **4 200 €** |

**Remises structurelles** (à afficher, elles rassurent et accélèrent la décision) :
- 2ᵉ module : **−15 %** · 3ᵉ et suivants : **−25 %** (le socle est amorti, la marge est là).
- Paiement comptant à la commande : **−5 %**.
- Association / petite commune (< 1 000 habitants) : **−10 %** — bon pour le bouche-à-oreille
  et les références.

---

## 3. Maintenance récurrente (le cœur du modèle)

C'est ici que se joue la valeur de l'entreprise. L'objectif est d'atteindre un revenu
mensuel récurrent qui couvre vos charges fixes — le développement devient alors du bonus.

| | **Maintenir** | **Évoluer** ⭐ | **Partenaire** |
|---|---|---|---|
| **Prix HT / mois** | **89 €** | **189 €** | **389 €** |
| Hébergement souverain (PaaS FR) | ✅ | ✅ | ✅ |
| Sauvegardes chiffrées quotidiennes + test de restauration trimestriel | ✅ | ✅ | ✅ |
| Mises à jour de sécurité (Flutter, dépendances, SDK iOS/Android) | ✅ | ✅ | ✅ |
| Supervision et alertes (disponibilité, erreurs) | ✅ | ✅ | ✅ |
| Correctifs bloquants | ✅ | ✅ | ✅ |
| Compatibilité nouvelles versions d'OS | ✅ | ✅ | ✅ |
| Gestion des comptes (Apple, Play, domaines, certificats) | — | ✅ | ✅ |
| Heures d'évolution incluses / mois | 0 | **2 h** (cumulables 6 mois) | **6 h** (cumulables 12 mois) |
| Délai de prise en charge (incident bloquant) | 48 h ouvrées | 24 h ouvrées | **4 h ouvrées** |
| Support | e-mail | e-mail + téléphone | e-mail + téléphone + espace dédié |
| Rapport d'usage trimestriel | — | ✅ | ✅ + recommandations |
| Veille réglementaire (RGPD, RGAA accessibilité) | — | information | **mise en conformité incluse** |
| Comité de suivi | — | annuel | **semestriel** |
| Réversibilité (remise du code + dump des données sur demande) | ✅ | ✅ | ✅ |

**Engagement et conditions**

- Durée : **12 mois** renouvelable tacitement ; 24 ou 36 mois sur demande.
- Paiement annuel d'avance : **−10 %** (189 € → 170 €/mois). Excellent pour la trésorerie.
- Revalorisation annuelle : **+3 % maximum** à la date anniversaire.
- Heures d'évolution non consommées : cumulables, **non remboursables** (standard).
- Hors forfait : **85 € HT/heure**, devis au-delà de 4 h.
- Sans contrat de maintenance : intervention facturée **120 € HT/heure** avec un minimum
  d'une heure — c'est ce qui rend l'abonnement évident.

---

## 4. Compte de résultat simplifié

### Ce que coûte réellement un client (plan lean)

| Poste | Coût mensuel |
|---|---|
| Hébergement PaaS (Scalingo/Clever Cloud, mutualisé ou dédié client) | 7 – 20 € |
| Tokens IA (production + évolutions) | 1 – 15 € |
| Sauvegarde (bucket R2/S3, quelques Go) | < 1 € |
| Supervision, domaine, certificats | ~2 € |
| **Coût direct total** | **10 – 38 €** |
| **Marge sur un contrat « Évoluer » à 189 €** | **151 – 179 € (80 – 95 %)** |

### Seuil de rentabilité

| Charges fixes mensuelles de l'agence (structure solo, lean) | Montant |
|---|---|
| Outils (dépôt privé, domaines, comptes développeurs) | ~30 € |
| API de tokens (toute activité confondue) | ~30 € |
| Assurance RC professionnelle | ~40 € |
| Comptable / banque / divers | ~60 € |
| **Total** | **~160 €/mois** |

**Il suffit de 2 contrats « Évoluer » pour couvrir l'intégralité des charges fixes.**
À 20 clients, le revenu récurrent est de ~3 800 €/mois **avant toute nouvelle vente** —
c'est à ce moment-là, et pas avant, qu'un serveur GPU devient un achat raisonnable.

> Comparaison : avec le plan initial, il fallait vendre **~1 application par mois rien que
> pour payer l'infrastructure**. Ici, deux abonnements suffisent. C'est toute la différence
> entre une structure qui survit et une structure qui grandit.

---

## 5. Conditions commerciales et clauses à sécuriser

**Facturation de la création**
- 30 % à la commande · 40 % à la recette · 30 % à la mise en production.
- Pour une mairie : acompte possible (avance forfaitaire), et les 30 % restants à la
  réception — prévoir une **procédure de recette écrite** (c'est ce qui évite les
  allers-retours infinis).

**Propriété et réversibilité** — votre meilleur argument face à un élu méfiant
- Le client est **propriétaire du code** de son application (sauf le socle, concédé en
  licence d'utilisation — précisez-le explicitement).
- Clause de réversibilité : sur demande, remise du dépôt et export complet des données
  dans un format ouvert, sous 30 jours.
- Cette clause vous coûte zéro (vous avez déjà le code) et lève l'objection numéro un :
  « et si vous disparaissez ? »

**RGPD — à traiter comme un livrable, pas comme une contrainte**
- Contrat de sous-traitance (art. 28 RGPD) fourni systématiquement, en annexe.
- Registre des traitements et durées de conservation livrés avec l'app.
- Données hébergées **en France**, chez un hébergeur certifié (Scalingo affiche ISO 27001,
  HDS et un socle SecNumCloud [comparatif](https://www.capterra.fr/compare/173415/1023596/clever-cloud/vs/scalingo)).
- Engagement écrit : **aucune donnée client n'est utilisée pour entraîner un modèle**, et
  les prestataires d'IA sollicités ne réutilisent pas les prompts (c'est le cas de
  Scaleway et de Mistral).
- Pour tout traitement de données sensibles (signalement géolocalisé, cantine, santé),
  proposer l'**AIPD** en prestation facturée : 750 €. C'est un différenciateur, pas une corvée.

**Ce qui n'est jamais inclus** (à écrire noir sur blanc)
- Création de contenu (textes, photos, catalogue produits) au-delà d'un jeu d'essai.
- Achats de tiers (compte Apple 99 €/an, Play 25 $ unique, SMS, cartographie au-delà du
  quota gratuit, passerelle de paiement).
- Refonte graphique, changement de positionnement, nouvelles intégrations tierces.
- Formation au-delà de 2 heures (facturée 85 €/h).

**Erreurs de tarification à ne pas commettre**
1. **Vendre des heures.** Vendez un résultat (« votre app de signalement en ligne en 4
   semaines »). Le client achète une certitude, pas du temps.
2. **Faire un devis gratuit détaillé de 12 pages.** Un devis d'une page, trois lignes,
   signé en réunion. Le CDC complet est *facturé* (500 €, déduits si la commande suit).
3. **Négocier le prix.** Négociez le périmètre : « on retire le module cantine, on le fera
   au deuxième trimestre. » Le prix reste, la relation aussi.
4. **Oublier l'indexation et l'engagement de durée** : sans eux, votre récurrence n'est
   qu'une succession de one-shots.

---

## 6. Ce qu'il faut absolument refacturer

Ne jamais absorber ces lignes : elles sont la preuve que vous gérez l'infrastructure.

| Poste | Coût réel | Refacturé |
|---|---|---|
| Compte Apple Developer | 99 $/an | 99 €/an (dans « Évoluer » ou en option iOS) |
| Compte Google Play | 25 $ unique | 25 € (dans la création) |
| Hébergement de production | 7 – 20 €/mois | inclus dans la maintenance |
| Nom de domaine | ~12 €/an | inclus dans la maintenance |
| SMS de notification (au-delà de 100/mois) | ~0,05 €/SMS | 0,08 €/SMS |
| Passerelle de paiement | 1,4 – 2,9 % | à la charge du client (compte direct) |

---

## 7. Plan d'action commercial (30 jours)

| Semaine | Action | Objectif |
|---|---|---|
| S1 | 10 communes de 1 000 à 8 000 habitants ciblées ; appel au secrétariat de mairie (pas au standard) | 3 rendez-vous |
| S2 | Démonstration du module signalement sur un cas réel (photo d'un lampadaire cassé, géoloc, back-office) | 1 devis envoyé |
| S3 | Relance avec l'argument seuil 60 000 € + clause de réversibilité | 1 signature |
| S4 | Livraison du socle en PWA pour le premier client ; demande de recommandation à 2 mairies voisines | 2 prospects entrants |

Un seul client « Évoluer » signé couvre vos charges fixes. Deux couvrent vos charges et
votre temps de prospection. C'est le seul jalon qui compte.
