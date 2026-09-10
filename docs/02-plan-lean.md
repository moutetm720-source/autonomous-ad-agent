# Le plan « lean » : la même usine logicielle, sans immobilisation

**Principes directeurs**

1. **Aucun coût fixe avant le premier euro de chiffre d'affaires.** Tout ce qui se loue à
   l'heure devient une dette ; tout ce qui se paie au token est une charge proportionnelle.
2. **Vendre avant de construire.** Le premier livrable est un devis signé, pas un serveur.
3. **Ce qui se répète va dans Git.** Prompts, enchaînements d'agents, gabarits Flutter :
   versionnés, revus, réutilisables. Ce qui est dessiné dans une UI est perdu.
4. **Le déterminisme d'abord, l'IA ensuite.** Analyse statique, tests, scan de secrets :
   gratuits et fiables. Le LLM corrige ce qu'ils trouvent.
5. **Le GPU se mérite.** On l'achète quand la facture de tokens le justifie, pas avant.

---

## Phase 0 — Semaine 1 : prouver qu'on peut vendre (budget : 0 €)

**Objectif : 3 lettres d'intention ou 1 devis signé. Aucune ligne d'infrastructure.**

| Action | Coût |
|---|---|
| Stack IA : API souveraine au token (Scaleway / Mistral) ou palier gratuit | 0 € |
| Orchestration : scripts Python dans ce dépôt + Open WebUI en local | 0 € |
| Mémoire : Qdrant en local, derrière Caddy (`stack-lean/`) | 0 € |
| CI/CD : GitHub Actions (dépôt public) ou 2 000 min/mois offertes (privé) | 0 € |
| Builds iOS : Codemagic, **500 minutes/mois gratuites** sur machines M2 — **aucun Mac à acheter** [Codemagic](https://eliteai.tools/tool/codemagic) / [review 2026](https://makerstack.co/reviews/codemagic-review/) | 0 € |
| Hébergement des maquettes : GitHub Pages / Cloudflare Pages | 0 € |
| Nom de domaine | ~12 €/an |

**Livrables de la semaine**

- Le socle Flutter blanc démarré (voir § « socle » ci-dessous).
- 5 prompts d'agents versionnés dans `agents/` : PO, Dev, QA, Rédacteur-CDC, Reprise-de-code.
- Une page de démonstration hébergée gratuitement, à montrer en rendez-vous.
- Un CDC type « Mairie de Saint-Sulpice » généré, à emporter en mairie.

**Ce qu'on ne fait PAS :** louer un GPU, installer Langflow, acheter un serveur, rédiger 60
pages de documentation interne.

---

## Phase 1 — Semaines 2 à 6 : livrer la première application (budget : ~140 €)

| Poste | Coût | Note |
|---|---|---|
| Tokens (≈5 M tokens, modèle courant) | **~3 €** | ~0,21 à 0,60 €/M |
| Compte Google Play (unique) | **25 $** | une seule fois [détail](https://appledaily.com/app-publishing-cost-google-play-apple-store/) |
| Compte Apple Developer | **99 $/an** | **à ne payer qu'au moment de publier sur iOS** |
| Hébergement client (PaaS FR) | **6 à 20 €/mois** | Scalingo dès 7,20 €/mois (ISO 27001, HDS, socle SecNumCloud) ou Clever Cloud dès 5,60 €/mois [comparatif](https://www.capterra.fr/compare/173415/1023596/clever-cloud/vs/scalingo) |

**Économie immédiate : 1 500 €.** Une commune ou un restaurant n'a pas besoin des deux
stores le premier jour. **Livrez en PWA (Flutter Web) + Android : 25 $ au total, zéro Mac,
zéro compte Apple.** L'iOS ne se justifie que si le client le demande et le paie — et là,
les 99 €/an sont refacturés dans le contrat de maintenance.

> PWA = installable sur l'écran d'accueil, notifications push sur Android, mises à jour
> instantanées, aucun passage par un store. Pour un signalement citoyen ou un click & collect,
> c'est 90 % de la valeur perçue pour 5 % du coût.

**Refacturation à prévoir dès le devis :** compte Apple (99 €/an), hébergement (PaaS),
noms de domaine. Ce sont des lignes de la maintenance, pas des charges de l'agence.

---

## Phase 2 — Mois 2 à 6 : industrialiser la réutilisation (budget : 0 € de plus)

C'est la phase qui crée la marge. L'objectif est de faire passer le coût de production de
la 2ᵉ application à 40 % de la 1ʳᵉ, puis 15 % pour la 5ᵉ.

### Le socle Flutter blanc

Un seul dépôt, des *flavors* par client. Tout client nouveau = de la configuration, plus du
développement.

```
socle/
├── lib/
│   ├── core/          # thème MD3, router, DI, gestion d'erreurs, logging
│   ├── features/
│   │   ├── auth/          # login, réinitialisation, biométrie
│   │   ├── push/          # Firebase Cloud Messaging, abstraction du fournisseur
│   │   ├── offline/       # cache local + file d'attente de synchronisation
│   │   ├── signalement/   # photo + géoloc + envoi  ← module mairie
│   │   ├── reservation/   # prise de RDV           ← module PME
│   │   ├── fidelite/      # carte de fidélité      ← module commerce
│   │   └── cotisation/    # adhésion + don         ← module association
│   └── legal/         # consentement RGPD, politique de confidentialité, mentions
├── flavors/           # une config par client : couleurs, logo, API, commune
├── tools/             # scripts de génération d'un nouveau client (10 min)
└── ci/                # quality-gate.yml, builds stores
```

**Règles non négociables du socle** (c'est ce qui rend la maintenance tenable à 20 clients) :

- Clean Architecture (data / domain / presentation) et `flutter_bloc` — comme prévu au plan.
- **Aucune clé en dur** : `String.fromEnvironment()` ou `flutter_dotenv`, vérifié par
  `scripts/check_secrets.sh` en CI.
- **Offline-first** : une app de mairie est utilisée dans des zones sans réseau. Les
  signalements sont mis en file d'attente et synchronisés.
- **Fournisseurs abstraits** : push, paiement, carte, notifications. Un client veut changer
  de prestataire de paiement ? Une classe à remplacer, pas une app à refaire.
- **Un générateur de client** (`tools/new_client.dart`) : en partant des couleurs, du logo
  et de l'URL d'API, il produit une app compilable en 10 minutes.

### Les agents passent dans le dépôt

Trois fichiers de prompts versionnés, plus un script d'enchaînement. Plus besoin de
Langflow : `python3 agents/run.py --projet mairie-saint-sulpice` exécute PO → Dev → QA,
écrit les livrables dans `clients/<nom>/`, et s'arrête à la première étape qui échoue.

```
agents/
├── product_owner.md      # génère le CDC + le registre RGPD
├── lead_developer.md     # génère le code Flutter, contraint par le socle
├── qa_cybersec.md        # corrige ce que la CI a trouvé
└── run.py                # enchaînement, budgets, journalisation des coûts
```

### Acquisition à coût nul : réutiliser `autonomous-ad-agent`

Le prototype déjà présent dans ce dépôt fait exactement ce qu'il faut pour exister
gratuitement sur des requêtes locales :

- `keywords.py` → variantes long-traîne : « application mobile mairie Saint-Sulpice »,
  « click and collect restaurant Castres », « signalement voirie commune Occitanie ».
- `generate_article.py` → pages de démonstration par verticale (mairie, restaurant,
  association), chacune avec son cas d'usage et un formulaire de contact.
- `.github/workflows/deploy.yml` → publication automatique sur GitHub Pages, **0 €**.

**Ce qu'il faut améliorer sur le prototype** pour qu'il serve une agence sérieuse :
remplacer la génération heuristique (phrases creuses) par un appel à un petit modèle via
LiteLLM, avec vos vrais cas clients en contexte ; ajouter les données structurées
(`LocalBusiness` en JSON-LD) ; et limiter le rythme de publication pour rester qualitatif.
Une vingtaine de pages de qualité, sur des requêtes à faible concurrence, suffisent à
déclencher les premiers appels entrants — c'est de l'acquisition à 0 €.

### La QA devient déterministe

`ci/quality-gate.yml` + `scripts/check_secrets.sh`, **gratuits**. Le budget tokens n'est
plus dépensé à chercher des fautes mais à les corriger.

---

## Phase 3 — 7 clients récurrents et au-delà : là seulement, envisager du matériel

Le signal de bascule est chiffré, pas émotionnel : **quand la facture de tokens dépasse
durablement 300 €/mois** (≈ 600 millions de tokens, donc une activité réellement
industrialisée), le self-hébergement commence à se discuter.

Trois paliers, dans cet ordre :

| Palier | Investissement | Pertinent quand |
|---|---|---|
| **1. GPU à l'usage** (loué, allumé/éteint) | 34 €/mois à 40 h (L4) | Dès que vous voulez tester un modèle local sans engagement |
| **2. Poste de travail d'occasion** (RTX 3090 24 Go ~ 700 €) | ~55 €/mois amorti + électricité | Modèle de brouillon local, embeddings locaux : **~80 % des appels** |
| **3. Serveur on-premise / cloud dédié** | 6 000 à 12 000 € | Volume > 600 M tokens/mois ET CA récurrent > 15 k€/mois |

Le palier 2 est le meilleur rapport valeur/prix : un 27B quantifié tourne sur 24 Go et
absorbe les tâches simples (formatage, commentaires, tests, résumés, embeddings). Vous
gardez l'API pour les tâches dures. **C'est ce panachage qui fait baisser la facture, pas
le remplacement intégral.**

---

## Ce que ce plan ne sacrifie pas

| Argument du plan initial | Statut dans le plan lean |
|---|---|
| Souveraineté des données | **Préservée** : API hébergées en France (Scaleway, Mistral), sans réutilisation des prompts ; option locale quand le volume le justifie |
| Modèles open-weights | **Améliorés** : accès au frontière 2026 au lieu d'un modèle de 2024 |
| RAG sur les connaissances | **Enfin fonctionnel** : modèle d'embedding déployé, dimension détectée |
| Sécurité | **Renforcée** : plus rien d'exposé sans auth, secrets scannés en CI, sauvegardes réellement chiffrées |
| Migration on-premise ultérieure | **Toujours possible** : Docker Compose conservé, LiteLLM permet de basculer un modèle sans toucher au code |
| Agents PO / Dev / QA | **Conservés**, mais versionnés dans Git au lieu d'être dessinés dans une UI |

---

## En résumé

| | Plan initial | Plan lean |
|---|---|---|
| Argent dépensé avant le premier client | 700 – 2 400 € | **~135 €** |
| Délai avant première mise en production | 3 – 6 semaines | **10 – 15 jours** |
| Coût IA par application livrée | 620 €+ (quote-part GPU) | **1 – 15 €** |
| Risque financier | Immobilisation | **Quasi nul** |
| Point de bascule vers le matériel | Jour 1 | **~10 clients récurrents** |

Le plan initial n'était pas faux : il était **prématuré**. Il décrivait l'outillage d'une
agence qui a déjà 15 clients. Construisez l'agence d'abord ; la forge suivra, payée par
les clients.
