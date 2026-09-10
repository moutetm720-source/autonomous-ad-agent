# Analyse critique du plan « agence de développement IA »

**Objectif de ce document :** identifier ce qui, dans le plan validé, consomme du capital
avant le premier euro de chiffre d'affaires — et proposer une version qui produit la même
chose pour 30 à 100× moins d'investissement, sans rien perdre sur l'argument souveraineté.

Chiffres produits par `outils/calcul_couts.py` (exécutable, modifiable) — prix publics
constatés en septembre 2026.

---

## 1. Verdict en 8 lignes

| # | Constat | Impact |
|---|---------|--------|
| 1 | Le plan engage **620 € à 2 190 €/mois de GPU avant le premier client** | Trésorerie brûlée |
| 2 | Le modèle choisi (DeepSeek-Coder-V2, 2024) a **2 générations de retard** | Qualité de code dégradée |
| 3 | Aucun modèle d'**embedding** n'est déployé → **le RAG ne peut pas fonctionner** | Qdrant inutile en l'état |
| 4 | **Langflow exposé sur Internet sans auth** : RCE non authentifiée, CVSS 9.8, exploitée dans la nature | Risque critique |
| 5 | Qdrant exposé sans clé API → fuite de données clients = **sinistre RGPD** | Risque critique |
| 6 | Les 2 scripts fournis contiennent **3 bugs bloquants** (dont un qui empêche toute sauvegarde) | Fausse sécurité |
| 7 | L'« agent QA cybersec » peut être remplacé par une CI **gratuite et déterministe** | Coût et aléa supprimés |
| 8 | Le vrai levier de marge n'est **pas le GPU**, c'est le **socle de code réutilisable** + la récurrence | Là est l'argent |

**Le point décisif :** à votre volume réel (5 à 60 millions de tokens/mois), une API
souveraine coûte **2,50 € à 30 €/mois**. Le seuil à partir duquel un GPU 24/7 devient
rentable est de **~1 000 millions de tokens/mois**. Vous en êtes **30 à 200× en dessous**.
Le GPU est un achat de confort, pas un achat de rentabilité — et certainement pas un
prérequis pour signer la première mairie.

---

## 2. Ce qui est bon dans le plan et qu'il faut garder

Avant de démonter, ce qui est juste :

- **Flutter/Dart** : excellent choix. Un seul code source → iOS, Android, Web. Le typage
  strict de Dart est un vrai avantage : les erreurs sont détectées par le compilateur,
  donc un agent IA peut itérer seul jusqu'au build vert.
- **L'argument souveraineté pour les mairies** : c'est le meilleur angle commercial du plan.
  Une collectivité ne peut pas confier des signalements citoyens (données personnelles +
  géolocalisation) à une infra extra-européenne opaque. C'est un différenciateur défendable.
- **Docker Compose** : bonne décision. Elle rend l'option « on-premise » possible *plus tard*,
  sans refonte. Gardez-la, même en version allégée.
- **La séparation PO / Dev / QA** : très bonne. À conserver — mais comme *prompts et scripts
  versionnés dans le dépôt*, pas comme trois services qui tournent en permanence.
- **Le modèle économique** (création + abonnement) : c'est le bon. C'est lui qui crée la
  valeur de l'entreprise, pas l'infrastructure.

---

## 3. Les 7 problèmes, en détail

### 3.1 Du coût fixe avant du chiffre d'affaires

Le plan démarre par « Cloud souverain avec GPU dédiés ». C'est un loyer qui court dès le
jour 1, que vous ayez 0 ou 10 clients.

| Carte (France) | €/heure | **24/7 (730 h)** | Ce qu'elle peut réellement charger |
|---|---|---|---|
| L4 24 Go | ~0,85 | **620 €/mois** | Qwen 3.6 27B (~17 Go) — correct, pas frontière |
| L40S 48 Go | ~1,50 | **1 095 €/mois** | Qwen3-Coder 80B-A3B (~48 Go) — ~96 % du frontière |
| H100 80 Go | ~3,00 | **2 190 €/mois** | Devstral-2 123B / GLM quantifié — quasi frontière |

Prix GPU France : L4 ~0,75–0,91 €/h, H100 ~2,75–3,83 €/h selon fournisseur
[gpus.io](https://gpus.io/en/providers/scaleway) / [lecompute.fr](https://lecompute.fr/couts/gpu-cloud-france-europe/).
Empreinte mémoire des modèles : [Local AI Report #2](https://llmconfigurator.com/en/reports/issue-2-best-open-source-coding-models-2026).

Ajoutez le VM d'orchestration, le stockage et les snapshots : **~700 à 2 400 €/mois de
charges fixes, avant le premier devis signé.** À 2 900 € une application, il faut vendre
une app par mois rien que pour payer l'infrastructure.

**Face à cela, le coût variable :**

| Modèle (hébergé UE, open-weights) | Entrée $/M | Sortie $/M | Mixte €/M |
|---|---|---|---|
| Scaleway `mistral-small-3.2-24b` | 0,17 | 0,40 | **0,21 €** |
| Scaleway `gpt-oss-120b` | 0,17 | 0,69 | **0,28 €** |
| Mistral `Codestral` | 0,30 | 0,90 | **0,41 €** |
| Scaleway `qwen3.6-35b-a3b` | 0,29 | 1,73 | **0,60 €** |
| Mistral `Large 3` | 0,50 | 1,50 | **0,69 €** |
| Scaleway `glm-5.2` (frontière) | 2,08 | 6,34 | **2,89 €** |

Sources : [Scaleway (catalogue Eden AI)](https://www.edenai.co/providers/scaleway),
[Mistral](https://benchlm.ai/mistral/api-pricing). Scaleway indique ne pas collecter, lire,
réutiliser ni analyser les prompts et les sorties — **l'argument souveraineté est donc
préservé sans posséder le GPU**. Mistral propose en outre un palier gratuit
« Experiment » (~1 Md de tokens/mois) pour démarrer à 0 €
[pricepertoken](https://pricepertoken.com/endpoints/mistral/free).

**Ce que ça donne concrètement :**

| Profil d'activité | GPU 24/7 | API souveraine | Gagnant |
|---|---|---|---|
| Bootstrapping (~5 M tokens/mois) | 620,50 € | **2,53 €** | API |
| 1 client actif (~20 M) | 620,50 € | **10,12 €** | API |
| 3 clients actifs (~60 M) | 1 095 € | **30,36 €** | API |
| Usine à plein régime (~200 M) | 2 190 € | **101,20 €** | API |
| Volume industriel (~600 M) | 2 190 € | **303,60 €** | API |

**Une application Flutter complète (≈5 M tokens d'allers-retours agents) coûte entre 1 € et
3,50 € de tokens** — contre 2 900 € facturés. Le coût de l'IA est un arrondi dans votre
compte de résultat. Il ne justifie aucune immobilisation.

> **Si vous tenez au self-hosté**, alors louez à l'usage : allumez, générez, éteignez.
> À 40 h/mois réelles, le L4 tombe à **34 €/mois au lieu de 620 €** (18× moins).
> C'est la seule façon rationnelle de toucher au GPU avant d'avoir 10 clients récurrents.

### 3.2 DeepSeek-Coder-V2 : deux générations de retard

Le modèle maître du plan date de 2024. En 2026, le paysage open-weights est ailleurs :
les meilleurs codeurs ouverts dépassent 80 % sur SWE-bench Verified
([llm-stats](https://llm-stats.com/leaderboards/open-llm-leaderboard) ; en janvier 2026,
GLM-4.7 était déjà à 73,8 % et DeepSeek V3.2-Speciale à 73,1 %
[comparatif](https://aarambhdevhub.medium.com/open-source-ai-vs-paid-ai-for-coding-the-ultimate-2026-comparison-guide-ab2ba6813c1d)).

**Et surtout : les modèles frontière ne tiennent pas sur un L4.** DeepSeek V4.1-Pro et
GLM-5.2 demandent ~400 Go de VRAM, Qwen3-Coder 480B ~270 Go
[Local AI Report #2](https://llmconfigurator.com/en/reports/issue-2-best-open-source-coding-models-2026).
Un L4 (24 Go) hébergera tout au plus un 27B quantifié.

**Conséquence :** le plan tel qu'écrit vous fait payer 620 €/mois pour héberger un modèle
qui est à la fois *obsolète* et *incapable de faire tourner son remplaçant*. C'est le pire
des deux mondes. Le raisonnement « j' aurai un meilleur modèle en local qu'en API » n'est
vrai qu'à partir d'un serveur à ~10 000 € — donc après le seuil de rentabilité, pas avant.

### 3.3 Le RAG ne peut pas fonctionner en l'état

Deux erreurs combinées dans `init_qdrant.py` :

1. **Aucun modèle d'embedding n'est déployé** dans le `docker-compose.yml`. vLLM sert
   `DeepSeek-Coder-V2`, un modèle de *génération de code*. Il n'y a nulle part de quoi
   transformer un PDF de délibération municipale en vecteur. Qdrant est donc une base vide
   qui ne sera jamais remplie : le cœur du dispositif (votre avantage « connaissances
   réglementaires ») est inopérant.
2. **La dimension 768 est posée au hasard.** Elle doit être exactement celle du modèle
   d'embedding : 1024 pour `multilingual-e5-large`, `mistral-embed` ou BGE-M3 ; 768 pour
   `all-mpnet-base-v2`. Une dimension erronée = refus d'insertion, ou pire, silence.

→ Corrigé dans `stack-lean/init_qdrant.py` : la dimension est **détectée en interrogeant le
modèle**, plus jamais devinée.

### 3.4 Trois bugs bloquants dans les scripts fournis

| Fichier | Bug | Conséquence |
|---|---|---|
| `init_qdrant.py` | `QDRANT_URL = "http://localhost:6333"COLLECTION_NAME = ...` sur une seule ligne | **SyntaxError** : le fichier ne démarre pas |
| `backup_qdrant.sh` | URL snapshot écrite `.../collections/{COLLECTION_NAME}/snapshots` — **le `$` manque** | L'URL contient le nom de la variable en littéral → **le snapshot n'est jamais créé**, le script sort en erreur à chaque exécution |
| `backup_qdrant.sh` | Intitulé « Sauvegarde chiffrée », mais c'est un `tar.gz` **sans aucun chiffrement** | Une sauvegarde de données clients en clair |

Deux fragilités supplémentaires : `grep -o` pour parser du JSON (à remplacer par `jq`) et
un `sleep 3` qui « espère » que le snapshot est prêt (à remplacer par une attente active du
statut). Sans oublier l'absence de copie hors site : une sauvegarde sur le même disque que
la base n'est pas une sauvegarde.

→ Corrigé dans `stack-lean/backup_qdrant.sh` : chiffrement réel (`age`), copie S3/R2,
attente active, `jq`, alerte d'espace disque.

### 3.5 Exposition réseau : deux risques critiques

Le compose publie **5 ports sur l'hôte** (`8000`, `6333`, `6334`, `7860`, `3000`). Sur un
VPS cloud sans pare-feu strict, tout est atteignable depuis Internet :

- **Langflow (7860)** : CVE-2025-3248 — exécution de code à distance **non authentifiée**,
  CVSS **9.8**, ajoutée au catalogue KEV du CISA car **exploitée dans la nature** ; une
  seconde faille critique a suivi (CVE-2026-5027)
  [Censys](https://censys.com/advisory/cve-2025-3248) / [Picus](https://www.picussecurity.com/resource/blog/cve-2025-3248-cve-2026-5027-langflow-rce).
  Exposer Langflow sans authentification = donner un shell sur votre serveur.
- **Qdrant (6333/6334)** : **aucune authentification par défaut**. N'importe qui peut lire,
  modifier ou supprimer vos collections — donc les données de vos clients mairies. C'est un
  incident de sécurité au sens RGPD (art. 32 : sécurité du traitement).

Trois anomalies de configuration à corriger aussi :

- `LANGFLOW_DATABASE_URL=sqlite:///langflow.db` est un chemin **relatif** au répertoire de
  travail, alors que le volume est monté sur `/var/lib/langflow` → **vos flows sont perdus
  au redémarrage**.
- `OPENAI_API_KEY=vllm-agence-secret-token` côté Open WebUI, mais vLLM est lancé **sans
  `--api-key`** : la clé n'est vérifiée par personne. Authentification factice.
- `--trust-remote-code` exécute du code arbitraire issu du dépôt du modèle. À réserver à
  un modèle dont on maîtrise la provenance.

### 3.6 Langflow est un mauvais choix pour une structure d'une à deux personnes

Au-delà du risque sécurité, l'orchestrateur visuel coûte cher en ressources (JVM/Python,
~2 Go de RAM au repos) pour dessiner ce qu'un script Python de 200 lignes exprime aussi
bien. Et surtout : **ce qui est dessiné dans une UI n'est pas versionné, pas revu, pas
reproductible.** Votre valeur, ce sont vos prompts et vos enchaînements d'agents — ils
doivent vivre dans Git, pas dans une base SQLite sur un conteneur.

### 3.7 L'agent QA « hacker éthique » est remplacé par une CI gratuite et déterministe

Un LLM qui relit du code pour y trouver des secrets est **non déterministe** : il en manque
une partie, il en invente d'autres, on ne peut pas l'auditer, et il coûte des tokens à
chaque exécution. Or tout ce qu'on attend de lui existe déjà sous forme d'outils gratuits :

- `flutter analyze --fatal-infos` — erreurs de typage et de null-safety
- `flutter test --coverage` + seuil de couverture
- `dart format --set-exit-if-changed` — style uniforme
- `scripts/check_secrets.sh` — secrets codés en dur (regex, 100 % déterministe)
- `gitleaks` — scan de l'historique Git
- `osv-scanner` / `trivy` — vulnérabilités connues dans les dépendances

→ Fourni dans `ci/quality-gate.yml` et `scripts/check_secrets.sh`. **Coût : 0 €** sur un
dépôt public, et 2 000 minutes/mois offertes sur un dépôt privé. Le LLM ne sert plus qu'à
*corriger* ce que ces outils ont trouvé — c'est son meilleur usage, et le seul qui soit
rentable.

---

## 4. Le vrai levier : ce n'est pas le GPU, c'est la réutilisation

Un GPU réduit le coût d'une ligne de code. Il ne réduit pas le coût d'acquisition d'un
client, ni le temps passé à recueillir un besoin, ni la durée d'une recette. Or dans une
app facturée 2 900 €, **les tokens représentent ~3 €**. Les 2 897 € restants, c'est du
temps humain et du commercial.

Les trois seuls leviers qui comptent :

1. **Un socle Flutter blanc réutilisable** (auth, push, RGPD, offline-first, CI, thème
   marque blanche). La 1ʳᵉ app coûte 100 % ; la 2ᵉ, 40 % ; la 5ᵉ, 15 %. C'est *ça*, votre
   « usine logicielle » — pas vLLM.
2. **La récurrence** : un abonnement de maintenance transforme un client one-shot en
   revenu prévisible. 20 clients × 149 €/mois = 2 980 €/mois récurrents, avant toute
   nouvelle vente.
3. **L'acquisition à coût nul** : le prototype `autonomous-ad-agent` déjà présent dans ce
   dépôt génère des pages SEO/locales automatiquement et les déploie gratuitement sur
   GitHub Pages. C'est exactement l'outil qu'il vous faut pour exister sur
   « application mobile mairie + nom de commune » avant d'avoir un budget marketing.

---

## 5. Chiffrage comparatif des trois scénarios

| | **A. Plan initial** | **B. Lean (recommandé)** | **C. Lean + GPU à l'usage** |
|---|---|---|---|
| Infra IA | vLLM + GPU 24/7 | API souveraine au token | API + GPU allumé 40 h/mois |
| Coût mois 1 | 700 – 2 400 € | **0 – 30 €** | ~35 – 60 € |
| Coût à 10 clients | 700 – 2 400 € | ~50 – 120 € | ~80 – 200 € |
| Qualité du modèle | 2024, bridé par 24 Go | **Frontière 2026 à la demande** | Frontière + local |
| Souveraineté | Totale | **UE, sans réutilisation des prompts** | UE + local |
| Temps de mise en route | 1 à 3 semaines (drivers, CUDA, NCCL, VRAM) | **1 journée** | 2 jours |
| Maintenance | Mises à jour GPU, OOM, VRAM | **Aucune** | Faible |
| Risque | Immobilisation avant CA | Quasi nul | Faible |

**Recommandation : démarrer en B.** Basculer en C (ou en on-premise) le jour où la facture
de tokens dépasse durablement 300 €/mois — ce qui correspond à ~10 clients actifs, donc à
une trésorerie qui le permet. À ce moment-là, l'investissement est financé par le chiffre
d'affaires au lieu de le précéder.

---

## 6. Suite

- **`docs/02-plan-lean.md`** — le plan d'exécution en 4 phases, de 0 € au premier client.
- **`docs/03-grille-tarifaire.md`** — la grille tarifaire et le contrat de maintenance
  (c'est le levier n°2 : il finance tout le reste).
- **`stack-lean/`** — la stack corrigée et allégée, prête à l'emploi.
- **`scripts/` et `ci/`** — la QA déterministe et gratuite.
