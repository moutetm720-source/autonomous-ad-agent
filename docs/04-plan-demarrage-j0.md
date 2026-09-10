# Plan de démarrage — de zéro au premier client récurrent (J0 → J+120)

**Point de départ :** aujourd'hui, **jeudi 10 septembre 2026**. Rien n'existe : pas de
structure, pas de client, pas de code. Ce plan va jusqu'au **vendredi 8 janvier 2027**.

---

## Règle d'or du plan

> **Aucune dépense avant un engagement client.**
> Tout ce qui peut se faire gratuitement se fait gratuitement. Tout ce qui coûte de l'argent
> attend d'être payé par un acompte. Un euro dépensé avant le premier virement est un euro
> qui manquera dans trois mois.

Conséquence directe : **pas de serveur, pas de GPU, pas de Mac, pas de logo payé, pas de
site web à 3 000 €.** On vend d'abord, on s'équipe ensuite, avec l'argent des clients.

---

## 1. Le budget de démarrage réel

| Poste | Coût | Quand | Obligatoire ? |
|---|---|---|---|
| Immatriculation (guichet unique / INPI) | **0 €** | Semaine 1 | Oui |
| Compte bancaire pro en ligne | **0 – 15 €/mois** | Semaine 1 | Oui dès le 1ᵉʳ encaissement |
| Assurance RC professionnelle | **~320 €/an** | Semaine 1 | Oui (exigée par les mairies) |
| Compte Google Play | **25 $** une fois | Au 1ᵉʳ client Android | Oui |
| Compte Apple Developer | **99 $/an** | Uniquement si iOS demandé | Non |
| Nom de domaine | **~12 €/an** | Semaine 1 | Oui |
| Outils (dépôt privé, CI) | **0 €** (Free tiers) | Semaine 1 | Non |
| Tokens IA | **0 – 30 €/mois** | À l'usage | Non |
| Hébergement des démos | **0 €** (GitHub Pages) | Semaine 2 | Oui |
| CFE (cotisation foncière) | **~300 €** | Exonéré l'année de création | — |
| Expert-comptable | **0 €** en micro la 1ʳᵉ année | Plus tard | Non |

**Budget de démarrage total : 0 € de fixe, ~360 € de frais incompressibles la première
année, et environ 135 € de débours au moment du premier client.**

Si vous possédez déjà un ordinateur capable de faire tourner Flutter (8 Go de RAM minimum,
16 Go recommandés), **vous n'avez besoin de rien d'autre.**

---

## 2. Semaine 1 (10 → 17 septembre) : exister légalement

L'objectif de la semaine : pouvoir émettre un devis qui engage, et être payé légalement.

### Jour 1 — Immatriculation (2 heures, 0 €)

Démarche en ligne sur le **guichet unique de l'INPI** (`procedures.inpi.fr`). Pour une
entreprise individuelle sous le régime micro, l'immatriculation est **gratuite**.

**Le bon choix au démarrage : micro-entreprise.**

| Critère | Micro-entreprise | EURL / SASU |
|---|---|---|
| Coût de création | 0 € | ~300 – 800 € (ou 0 € en EI au réel) |
| Comptabilité | Déclaration de CA, rien d'autre | Comptable quasi obligatoire (~900 €/an) |
| Charges | ~28 % du **CA encaissé** | ~45 – 55 % du **bénéfice** |
| Plafond de CA | 83 600 € (services, 2026-2028) | Illimité |
| Charges déductibles | Non (abattement forfaitaire) | Oui |
| Rémunération | Tout le CA restant | Salaire ou dividendes |
| **Verdict** | **Parfait pour démarrer** | À envisager vers 60 000 € de CA |

Deux seuils à garder en tête, ils piloteront vos décisions de l'année :

- **83 600 € de CA** : plafond du régime micro pour les prestations de services (revalorisé
  pour 2026-2028) [economie.gouv.fr](https://www.economie.gouv.fr/entreprises/gerer-sa-micro-entreprise/micro-entreprises-quel-est-le-montant-de-vos-cotisations-sociales).
- **37 500 € de CA** : seuil de franchise de TVA. Au-delà, vous facturez HT + 20 %.
  Aucun impact de marge sur des clients professionnels, mais il faut l'anticiper dans les
  devis [Propulse by CA](https://propulsebyca.fr/actualites/nouveaux-plafonds-chiffre-affaires-2026-micro-entreprise).

> ⚠️ À 2 900 € l'application et 189 €/mois de maintenance, le seuil de TVA est atteint vers
> **8 clients**. Prévenez vos clients dès la signature : « le jour où je dépasse le seuil,
> la TVA s'ajoute au HT » — une phrase dans le devis vous évite un conflit.

**Deux cases à cocher impérativement :**

1. **L'ACRE**, demandée lors de la création. Attention : depuis le **1ᵉʳ juillet 2026**,
   l'exonération n'est plus que de **25 %** (au lieu de 50 %). Concrètement, votre taux de
   cotisations la première année passe de 25,6 % à **19,2 %** en BNC
   [economie.gouv.fr](https://www.economie.gouv.fr/entreprises/gerer-sa-micro-entreprise/micro-entreprises-quel-est-le-montant-de-vos-cotisations-sociales).
   C'est environ **1 900 € économisés sur 20 000 € de CA**. Ne pas la demander est une
   erreur qui ne se rattrape pas.
2. **La catégorie d'activité.** Un développeur relève normalement des **BNC** (profession
   libérale non réglementée), taux **25,6 %** en 2026 (décret n° 2025-943 du 8 septembre
   2025 — il était à 24,6 % en 2025)
   [l'Entreprise Facile](https://www.lentreprisefacile.fr/blog/cotisations-micro-entrepreneur-2026-reforme-taux/) /
   [Abby](https://abby.fr/guide/micro-entreprise/cotisations-sociales-auto-entrepreneur).
   Une prestation de services commerciale/artisanale (**BIC**) est à 21,2 %.
   **Faites-vous confirmer le bon classement par l'Urssaf ou votre CFE** : 4,4 points
   d'écart, c'est 880 € par an sur 20 000 € de CA.

### Jour 2 — Banque et assurance

- **Compte bancaire dédié** (obligatoire au-delà de 10 000 € de CA deux années de suite,
  mais prenez-le tout de suite : mélanger les flux est la première cause de redressement).
  Les banques pro en ligne facturent 0 à 15 €/mois.
- **RC professionnelle** : indispensable. Une mairie vous la demandera, un client privé
  peut vous la réclamer après un incident. Comptez ~320 €/an pour un prestataire
  informatique. Vérifiez que le contrat couvre bien « prestations de services informatiques
  et développement d'applications » — ce n'est pas automatique.

### Jour 3 — Le sésame pour les mairies : Chorus Pro

C'est le point que la plupart des créateurs découvrent trop tard.

**Depuis le 1ᵉʳ janvier 2020, toute facture destinée au secteur public (mairie, hôpital,
établissement public) doit être déposée sur Chorus Pro, et ce sans aucun seuil de montant**
[Remporte](https://remporte.fr/blog/chorus-pro-facturation-electronique-marche-public/).
Une facture PDF envoyée par e-mail à une mairie **n'est pas payable**. Donc :

1. Créez votre compte sur `chorus-pro.gouv.fr` avec votre SIRET (gratuit).
2. Notez dès maintenant les trois mentions qui font rejeter une facture et repartir le
   décompte à zéro : **le numéro de marché** (ou le numéro d'engagement), **le code service**
   de la collectivité, et **le numéro SIRET complet de l'entité publique**.
   Demandez-les au secrétariat de mairie **au moment de la commande**, pas à la facturation.
3. Délai de paiement légal : **30 jours** pour l'État et les collectivités.
   Prévoyez votre trésorerie en conséquence : acompte de 30 % obligatoire à la commande.

### Jour 4 — Le dossier « prêt à répondre »

Préparez une seule fois un dossier PDF de 4 pages que vous enverrez en pièce jointe à
chaque demande :

- Extrait RNE / avis de situation (à télécharger sur `annuaire-entreprises.data.gouv.fr`)
- **Attestation de vigilance Urssaf** — exigée par l'acheteur public dès que le contrat
  atteint **5 000 € HT** (contrat + avenants), à renouveler tous les 6 mois
  [OnceForAll](https://onceforall.fr/legislations/reglementations/obligation-vigilance/).
  Téléchargeable en 2 minutes sur votre espace Urssaf. **Régénérez-la tous les 6 mois,
  sinon votre facture sera bloquée.**
- Attestation d'assurance RC professionnelle à jour
- RIB professionnel

### Jour 5 — L'environnement de travail (0 €)

```bash
# Socle IA : aucune carte graphique requise
cd stack-lean && cp .env.example .env && docker compose up -d

# Dépôt privé + CI gratuite (GitHub : 2 000 min/mois offertes sur un dépôt privé)
git init socle-flutter && cd socle-flutter
cp ../ci/quality-gate.yml .github/workflows/

# Comptes : Scaleway (clé API) + Mistral (palier gratuit ~1 Md de tokens/mois)
```

### Ce qu'on ne fait PAS cette semaine

❌ Acheter du matériel · ❌ Créer un site vitrine · ❌ Faire faire un logo ·
❌ Rédiger une plaquette commerciale · ❌ Commander des cartes de visite ·
❌ Louer un serveur · ❌ Écrire le socle Flutter en entier

---

## 3. Semaine 2 (18 → 24 septembre) : une démo qui vend

Vous n'avez rien à montrer. Il vous faut donc **un produit de démonstration crédible en
5 jours**, pas un produit complet.

**Le périmètre de la démo :** une seule fonction, la plus visuelle — **le signalement
citoyen géolocalisé**. Un habitant photographie un lampadaire cassé, l'application
géolocalise, envoie, et le back-office de la mairie affiche le point sur une carte avec le
statut « pris en charge ». C'est tout. C'est ce qui déclenche « ah oui, ça nous servirait ».

| Jour | Livrable |
|---|---|
| J+8 | Projet Flutter initialisé, thème Material 3, deux écrans |
| J+9 | Prise de photo + géolocalisation + aperçu |
| J+10 | File d'attente hors ligne (le point technique qui impressionne en mairie) |
| J+11 | Back-office : liste + carte + changement de statut |
| J+12 | Déploiement en PWA sur GitHub Pages + compte de démonstration |

**Deux décisions qui vous font gagner des semaines :**

- **PWA d'abord.** Pas de store, pas de validation Apple, pas de Mac, pas de 99 €. Une URL,
  un raccourci sur l'écran d'accueil, et ça marche sur le téléphone du maire. Vous ajouterez
  Android (25 $) au premier client payant, et iOS seulement si on vous le demande.
- **Une démo par verticale.** Le module signalement est le même pour toutes les mairies ;
  seuls le logo, les couleurs et le nom changent. C'est déjà du réemploi.

**Le site de démonstration** : le prototype `autonomous-ad-agent` de ce dépôt génère et
publie des pages automatiquement sur GitHub Pages, **gratuitement**. Servez-vous-en pour
héberger votre démo et une page par verticale (mairie / commerce / association). Une URL à
envoyer par e-mail vaut mieux qu'une plaquette de 20 pages.

---

## 4. Semaines 3-4 (25 sept → 9 oct) : la prospection

### Cibler

| Cible | Pourquoi elle achète | Budget décideur | Cycle |
|---|---|---|---|
| **Mairie 1 000 – 8 000 hab.** | Obligation de service, proximité, élections | 2 000 – 10 000 € | 2 – 8 semaines |
| **Restaurant / commerce** | Perte de marge sur les plateformes de livraison (15 – 30 %) | 1 500 – 5 000 € | 1 – 4 semaines |
| **Association active** | Adhésions à relancer, dons à faciliter | 1 000 – 3 000 € | 2 – 6 semaines |

**Priorité : les mairies de 1 000 à 8 000 habitants.** Trois raisons : le budget existe et
est voté, la décision est concentrée sur une personne, et le seuil de 60 000 € HT (décret
n° 2025-1386) permet une commande directe sans appel d'offres — c'est votre avantage
décisif, documenté dans `docs/03-grille-tarifaire.md`.

### La méthode (30 communes en 2 semaines)

1. **Identifier.** 30 communes dans un rayon de 60 km. Site web de la mairie → nom du
   secrétaire général.
2. **Appeler le secrétariat, pas le standard.** « Bonjour, je développe des applications
   mobiles pour les collectivités locales. J'ai réalisé un module de signalement citoyen
   pour des communes de cette taille. Est-ce que Monsieur le Maire ou le secrétaire
   général aurait 15 minutes la semaine prochaine ? »
3. **Ne jamais présenter un catalogue.** Poser trois questions : *Qu'est-ce qui vous
   génère le plus d'appels aujourd'hui ? Combien de temps y passez-vous ? Si ça
   disparaissait demain, ça changerait quoi ?*
4. **Montrer, ne pas décrire.** Sortir son téléphone, faire un signalement en direct.
5. **Repartir avec une étape datée**, jamais avec « on va réfléchir ».

### Les chiffres de la prospection

Sur 30 communes contactées, comptez **8 à 10 conversations réelles, 3 à 4 rendez-vous,
1 à 2 devis, 1 signature**. C'est le ratio normal. L'échec du premier mois n'est pas un
échec commercial : c'est le taux de conversion du secteur public. **Tenez 90 jours avant
d'évaluer quoi que ce soit.**

### Le devis

Une page. Trois lignes. Pas de catalogue.

- Le problème reformulé en une phrase (leurs mots, pas les vôtres).
- La solution et sa date de mise en service.
- Le prix, en deux lignes : création (une fois) + maintenance (par mois).
- **La phrase qui débloque** : « Ce projet restant sous le seuil de 60 000 € HT, vous
  pouvez nous confier le marché directement, sans procédure de mise en concurrence. »
- Validité 30 jours, acompte 30 %.

Modèle prêt à remplir : `modeles/devis.md`.

---

## 5. J+30 → J+60 (10 oct → 9 nov) : signer et livrer le premier

### La semaine qui suit la signature

1. **Encaisser l'acompte (30 %).** Pas d'acompte, pas de démarrage. C'est la règle, même
   avec une mairie — l'acompte est un droit et une pratique courante en marché public.
2. **Rédiger le CDC en 48 h** avec l'agent Product Owner (`agents/product_owner.md`),
   le faire valider par écrit. **C'est le document qui arrête le périmètre** : tout ce qui
   n'y figure pas devient un avenant payant.
3. **Écrire la procédure de recette** avant de coder. C'est le document qui dit comment on
   constate que c'est fini. Modèle : `modeles/pv-recette.md`. Sans lui, un projet de
   2 900 € devient un projet de 2 900 € qui n'en finit pas.

### Le rythme de production

| Semaine | Ce qui doit être vrai |
|---|---|
| S1 post-signature | CDC validé, environnement du client créé, dépôt Git du client ouvert |
| S2 | Module principal fonctionnel en PWA, URL de préproduction envoyée au client |
| S3 | Retours du client intégrés, back-office livré, jeux d'essai |
| S4 | Recette contradictoire (1 h en visio), PV de recette signé, mise en production |

**Une démo toutes les semaines, même partielle.** Le silence de trois semaines est ce qui
tue la confiance. Une URL chaque vendredi, même moche, vaut mieux qu'un silence poli.

### Coût de revient de cette première application

| Poste | Coût |
|---|---|
| Tokens IA (~5 M) | 1 – 15 € |
| Compte Google Play | 25 $ (une fois) |
| Hébergement PaaS | 7 – 20 €/mois |
| **Total** | **~45 € la première année** |

C'est la démonstration la plus parlante de tout ce plan : **votre coût de production
technique est inférieur à 1,5 % du prix de vente.** Votre seule vraie dépense, c'est votre
temps. Optimisez le temps, pas les serveurs.

---

## 6. J+60 → J+90 (10 nov → 9 déc) : la récurrence, seul vrai enjeu

Une application vendue est un événement. Un abonnement signé est une entreprise.

**Ce que disent les chiffres** (`outils/simulateur_tresorerie.py`, barèmes 2026) :

| Scénario | CA annuel | Net mensuel (an 2) |
|---|---|---|
| 3 clients + 2 apps | 14 604 € | 710 € |
| 8 clients + 5 apps | 37 644 € | 1 992 € |
| 20 clients + 10 apps | 84 360 € | 4 555 € |

**Sur 100 € encaissés, il vous reste 58 à 65 €** une fois payées les cotisations
(25,6 %), la CFP (0,2 %), le versement libératoire (2,2 %) et vos frais professionnels.

**Et l'enseignement le plus important du simulateur** — celui qui doit dicter votre
grille tarifaire :

| Forfait | Contribution nette mensuelle | Contrats nécessaires pour 2 000 €/mois |
|---|---|---|
| Maintenir **89 €** | 44 € | **48 clients** |
| Évoluer **189 €** ⭐ | 116 € | **19 clients** |
| Partenaire **389 €** | 260 € | **9 clients** |

**Le forfait à 89 € est un piège : il faudrait 48 clients pour en vivre.** Gardez-le comme
offre d'appel pour les petites associations, mais **positionnez 189 € comme l'offre par
défaut** et orientez systématiquement la conversation vers elle. C'est 3 fois moins de
clients à trouver pour le même revenu.

### La mécanique de la récurrence

- Le contrat de maintenance est signé **en même temps que le devis de création**, jamais
  après. « Le prix comprend 12 mois de maintenance, reconductibles » → le client n'a pas à
  décider deux fois.
- **Prélèvement automatique** mensuel ou annuel. Un contrat qu'il faut relancer est un
  contrat qui meurt.
- À 10 clients, **l'équivalent d'une demi-journée par mois** suffit à la maintenance :
  mises à jour Flutter, surveillance, sauvegardes. C'est ce qui rend le modèle tenable seul.

---

## 7. J+90 → J+120 (10 déc → 8 jan) : répéter et industrialiser

Trois chantiers, dans cet ordre :

1. **Client 2 et 3**, avec le réemploi : la 2ᵉ application doit vous coûter **40 % de la
   1ʳᵉ**, la 3ᵉ **25 %**. Sinon, ce n'est pas une agence, c'est du sur-mesure.
2. **Le générateur de client** dans le socle (`socle/tools/new_client.dart`) : couleurs,
   logo et URL d'API → application compilable en 10 minutes.
3. **La recommandation** : chaque mairie livrée est un sésame vers les communes voisines.
   Un maire satisfait qui appelle son voisin vous économise trois semaines de prospection.

**À la fin du J+120, les objectifs :**

- [ ] 2 à 3 clients signés, dont 2 sous contrat de maintenance
- [ ] Socle réutilisable à 40 % du coût initial
- [ ] Une référence mairie documentée (capture d'écran + témoignage de 3 lignes)
- [ ] Chorus Pro maîtrisé (facture acceptée du premier coup)
- [ ] Un MRR ≥ 400 €

---

## 8. Les 5 indicateurs à suivre chaque vendredi

15 minutes, un tableur, 5 chiffres. Rien de plus.

| Indicateur | Objectif J+120 | Pourquoi |
|---|---|---|
| Conversations réelles / semaine | 5 | C'est le seul levier que vous contrôlez à 100 % |
| Devis envoyés (cumulés) | 8 | En dessous, c'est un problème de volume, pas de prix |
| MRR (revenu mensuel récurrent) | 400 € | C'est la valeur de l'entreprise |
| Coût de production de la dernière app | < 45 € | S'il grimpe, c'est que le socle n'est pas réutilisé |
| Temps passé par app (heures) | divisé par 2 vs la 1ʳᵉ | Le seul indicateur de productivité qui compte |

**Signaux d'alerte :** 3 semaines sans rendez-vous → changer de cible, pas de discours.
2 devis refusés sur le prix → revoir le périmètre, pas le tarif.

---

## 9. Les 6 risques et leurs parades

| Risque | Probabilité | Parade |
|---|---|---|
| **Aucune signature en 3 mois** | Élevée | Garder 6 mois de charges personnelles à côté ; viser d'abord les commerçants (cycle plus court) pour encaisser vite |
| **Le projet s'étire indéfiniment** | Élevée | CDC validé + PV de recette signé + périmètre écrit. Sans ça, un projet à 2 900 € devient un gouffre |
| **Facture rejetée par Chorus Pro** | Moyenne | Demander numéro d'engagement et code service **à la commande** |
| **Le client ne sait pas quoi vous demander** | Élevée | Vous posez 3 questions et proposez un périmètre. Ne jamais demander « qu'est-ce que vous voulez ? » |
| **Dépassement du seuil de TVA en cours d'année** | Moyenne | Clause dans le devis ; surveiller le CA cumulé chaque mois |
| **Vouloir tout construire avant de vendre** | **Très élevée** | C'est le risque principal. La parade est ce plan : une démo en 5 jours, puis vendre |

---

## 10. Ce qu'il faut refuser

- ❌ « On vous paiera à la mise en ligne » → acompte 30 % ou rien.
- ❌ Le projet « on verra le périmètre en cours de route » → CDC d'abord.
- ❌ « Faites-nous la même chose que l'application de [grande ville] » → ce projet coûte
  300 000 €, ce n'est pas votre marché.
- ❌ L'iOS avant d'avoir un client payant → 99 €/an et des semaines de validation.
- ❌ « On paiera en fin d'année sur le budget suivant » → devis daté, acompte, ou passage
  au client suivant.
- ❌ Le maintien en condition opérationnelle gratuit « pour voir » → c'est le contrat de
  maintenance, il est au tarif.

---

## 11. Calendrier récapitulatif

| Période | Dates | Objectif | Dépense |
|---|---|---|---|
| **S1 — Exister** | 10 → 17 sep | SIRET, banque, RC pro, Chorus Pro, stack IA | 0 € + 320 €/an |
| **S2 — Démontrer** | 18 → 24 sep | Module signalement fonctionnel en PWA | 0 € |
| **S3-S4 — Prospecter** | 25 sep → 9 oct | 30 communes, 4 RDV, 2 devis | 0 € |
| **J+30 — Signer** | 10 oct | Acompte encaissé, CDC validé | 0 € |
| **J+30→60 — Livrer** | 10 oct → 9 nov | Mise en production + PV de recette | ~45 € |
| **J+60→90 — Récurrence** | 10 nov → 9 déc | Contrat de maintenance actif, 2ᵉ client | 0 € |
| **J+90→120 — Industrialiser** | 10 déc → 8 jan | 3 clients, socle réutilisé, MRR 400 € | 0 € |

---

## 12. La journée type, quand l'agence tourne

| Horaire | Activité |
|---|---|
| 8 h 30 – 10 h 30 | Production (le cerveau est frais, le code d'abord) |
| 10 h 30 – 12 h | Prospection : appels, e-mails, relances. **Jamais l'après-midi.** |
| 14 h – 16 h | Production, recette, mises à jour clients |
| 16 h – 17 h | Support et maintenance (créneau unique : sinon le support mange la journée) |
| 17 h – 17 h 30 | Admin : factures, Chorus Pro, Urssaf, tableau de bord du vendredi |

**Deux règles de survie :** la prospection se fait le matin, parce qu'on remet toujours au
lendemain ce qui fait peur. Et le support a un créneau : répondre dans la minute à chaque
message, c'est ne jamais rien produire.

---

## 13. Checklist de démarrage (J0 → J+7)

Administratif
- [ ] Immatriculation déposée sur le guichet unique INPI
- [ ] **ACRE demandée lors de la création** (non rétroactive)
- [ ] Catégorie BNC / BIC confirmée auprès de l'Urssaf
- [ ] Compte bancaire dédié ouvert
- [ ] RC professionnelle souscrite, mention « prestations informatiques » vérifiée
- [ ] Compte Chorus Pro créé, SIRET rattaché
- [ ] Attestation de vigilance Urssaf téléchargée (à renouveler tous les 6 mois)
- [ ] Dossier « prêt à répondre » assemblé en un seul PDF

Technique
- [ ] `stack-lean` démarré, clés API Scaleway et/ou Mistral configurées
- [ ] Dépôt Git du socle créé, `ci/quality-gate.yml` actif
- [ ] `scripts/check_secrets.sh` en pré-commit
- [ ] Compte Google Play en cours de création (25 $)
- [ ] Domaine réservé, GitHub Pages prêt

Commercial
- [ ] 30 communes listées dans un tableur avec nom du contact
- [ ] Script d'appel relu à voix haute trois fois (`modeles/prospection.md`)
- [ ] Démo PWA accessible par URL publique
- [ ] Devis type prêt à remplir (`modeles/devis.md`)

---

> **Un dernier mot.** Ce plan ne demande ni investissement, ni associé, ni local, ni
> matériel. Il demande 90 jours de prospection régulière — ce qui est infiniment plus
> difficile que d'acheter un serveur. C'est pourtant la seule dépense qui produit du
> chiffre d'affaires.
