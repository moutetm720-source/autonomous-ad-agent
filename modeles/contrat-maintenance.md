# Contrat de maintenance — trame et clauses clés

> Document à faire relire par un professionnel du droit avant la première signature.
> Cette trame couvre les Points à ne pas oublier ; ce n'est pas un contrat prêt à signer.

---

## 1. Objet

Maintenance corrective, évolutive et hébergement de l'application {nom}, pour le compte de
{client}.

## 2. Durée et reconduction

- Durée initiale : **12 mois**, à compter de la mise en production.
- Renouvellement **par tacite reconduction** par périodes de 12 mois.
- Résiliation : courriel avec **préavis de 2 mois** avant l'échéance annuelle.
- Pas de résiliation anticipée sans paiement des mois restants, sauf manquement grave.

## 3. Prix et facturation

- {189} € HT / mois, prélevés le {1er} de chaque mois.
- Paiement annuel d'avance : **−10 %**.
- Revalorisation : **+3 % maximum** à chaque échéance annuelle.
- Retard de paiement : suspension du service **après relance restée sans effet 15 jours**,
  jamais avant. Une suspension brutale sur une application de mairie est un incident
  politique, pas un incident commercial.

## 4. Engagements de service (à adapter selon le palier)

| | Maintenir 89 € | Évoluer 189 € | Partenaire 389 € |
|---|---|---|---|
| Prise en charge incident bloquant | 48 h ouvrées | 24 h ouvrées | 4 h ouvrées |
| Heures d'évolution incluses | 0 | 2 h/mois | 6 h/mois |
| Cumul des heures | — | 6 mois | 12 mois |
| Support | e-mail | e-mail + téléphone | + espace dédié |

**Définition d'un incident bloquant** : l'application est indisponible ou une fonction
essentielle est inutilisable. **Ne sont pas bloquants** : une demande d'évolution, une
question d'usage, un défaut d'affichage mineur, un problème lié au terminal de l'utilisateur.

## 5. Ce qui est inclus

Hébergement en France · sauvegarde quotidienne chiffrée avec test de restauration
trimestriel · mises à jour de sécurité (Flutter, dépendances, SDK) · compatibilité avec les
nouvelles versions d'OS · supervision · correctifs · {gestion des comptes Apple/Play et des
certificats} · {rapport d'usage trimestriel} · {veille RGPD et accessibilité}.

## 6. Ce qui est exclu (à écrire noir sur blanc — c'est ce qui évite 90 % des conflits)

- Création de contenu au-delà d'un jeu d'essai
- Nouvelles fonctionnalités hors heures incluses : **85 € HT/heure**, devis au-delà de 4 h
- Refonte graphique, changement de positionnement, changement de nom
- Intégrations tierces non prévues (logiciel comptable, ERP, SI de la collectivité)
- Achats de tiers : compte Apple (99 €/an), Google Play (25 $ unique), SMS, cartographie
  au-delà du quota gratuit, passerelle de paiement
- Formation au-delà de 2 heures
- Intervention en dehors des heures ouvrées, sauf incident bloquant en palier Partenaire
- **Toute intervention liée à une modification du code par un tiers** — clause indispensable

## 7. Responsabilité et limites

- Obligation de **moyens**, pas de résultat.
- Plafond de responsabilité : **le montant des sommes versées sur les 12 derniers mois**.
  C'est la clause standard et la plus importante du contrat ; sans elle, un incident
  mineur peut coûter plus que la valeur de l'entreprise.
- Assurance RC professionnelle : {compagnie}, police n° {numéro}.
- Force majeure, dont les indisponibilités des fournisseurs d'hébergement et des stores.
- **Exclusion expresse des dommages indirects** : perte d'exploitation, perte de données non
  couverte par la sauvegarde, manque à gagner.

## 8. Données personnelles (client = responsable de traitement, vous = sous-traitant)

- Contrat de sous-traitance **art. 28 RGPD** en annexe, signé.
- Durées de conservation définies dans le registre, purges effectivement exécutées.
- Hébergement en France, chez un prestataire certifié.
- Engagement écrit : **aucune donnée client n'est utilisée pour l'entraînement d'un modèle**
  ; les prestataires d'IA sollicités ne réutilisent pas les prompts.
- Notification de toute violation de données dans les **72 heures**.
- Assistance à l'exercice des droits (accès, rectification, suppression).
- Sous-traitants ultérieurs : liste tenue à jour, information préalable du client.

## 9. Propriété et réversibilité

- Le client est **propriétaire du code** de son application spécifique.
- Le **socle technique commun** reste la propriété du prestataire, concédé en licence
  d'utilisation, non cessible, non exclusif. *(Clause à faire figurer explicitement : c'est
  la valeur de votre entreprise.)*
- **Réversibilité** : sur demande, remise du code et export des données dans un format
  ouvert dans les 30 jours. Gratuit la première année, puis sur devis.
- En cas de résiliation, les données sont effacées 90 jours après la restitution.

## 10. Clauses à ne jamais oublier

- **Indépendance des parties** : pas de subordination, pas de lien salarial. Indispensable
  quand on travaille avec des collectivités (risque de requalification en contrat de travail
  ou de délit de marchandage).
- **Confidentialité** réciproque.
- **Référence commerciale** : droit de citer le client (logo, témoignage) sauf opposition
  écrite — précieux pour convaincre les communes voisines.
- **Médiation de la consommation** : mention obligatoire si le client est un
  **non-professionnel** (un particulier). Les associations et les mairies sont des
  professionnels, mais certaines associations peuvent être requalifiées — mentionnez le
  médiateur par précaution, c'est gratuit.
- **Droit applicable et juridiction compétente**.

---

## Le conseil pratique

Faites signer le contrat de maintenance **en même temps que le devis de création**, sur le
même document. Un client qui a déjà accepté « 189 €/mois à partir de la mise en service »
ne remettra pas la décision en cause trois mois plus tard. Un client à qui vous présentez
l'abonnement après la livraison y voit une nouvelle dépense — et vous perdez 40 % des
contrats à ce moment-là.
