# Compte rendu des audits — pour validation dans l’orchestration

Généré le 2026-10-23T11:14:37+00:00. WORKING. **Production des projets/LAB suspendue dans l’attente de validation.** Les expériences déjà exécutées sont exploratoires et non validées. Ce document ne modifie aucun statut pédagogique du CORE.

## État de complétude

- Retail, Olist et MetroPT-3 : acquisition, SHA-256, CRC et audit exécutés.
- CFPB acquisition/intégrité : 21/21 archives téléchargées, SHA-256 calculés, CRC tous réussis ; 1 429 655 864 octets. Audit de contenu : **TERMINÉ sur les 21 exports officiels**. 17 533 918 lignes et 3 851 415 récits non vides dans les seuls exports audités avec succès. Le total couvre les 21 fichiers, pas un échantillon.
- Telco : dépôt non fourni ; aucune reconstruction.
- Publications externes, cloud, offre commerciale et dépenses : aucune action effectuée.

## PRJ2 — UCI Online Retail II

Source : https://archive.ics.uci.edu/dataset/502/online+retail+ii ; Chen, DOI 10.24432/C5CG6D. Licence officielle CC BY 4.0, attribution requise.

**Mesures.** 1 067 371 lignes d’articles, deux feuilles (525 461 et 541 910). Période réelle : 2009-12-01 07:45:00 à 2011-12-09 12:50:00. 34 335 répétitions exactes ; 243 007 identifiants client absents ; 4 382 descriptions absentes. 19 494 annulations à préfixe C ; 22 950 quantités <=0 ; 6 207 prix <=0. Ces groupes se recoupent et ne doivent pas être additionnés. La règle exploratoire prix/quantité positifs, sans C et sans répétitions exactes conserve 1 007 913 lignes et 104 semaines complètes.

**Gate 0.** Analyste de planification, décision hebdomadaire à horizon une semaine : préparer des scénarios de ventes observées et de charge. Abstention si extraction incomplète ; validation humaine. Coûts d’erreur inconnus. Aucun stock, rupture, marge ou capacité réelle : ne pas promettre optimisation de stock ni ROI.

**DPD/fuites.** Agrégation à la semaine ; variables et calibration limitées au passé. Historique limité à environ deux ans et un commerçant britannique ancien. Les doublons peuvent être des ventes légitimes : tester la sensibilité avant de retenir le nettoyage. Les retours exclus changent la cible ; ventes positives ≠ ventes nettes ≠ demande latente.

**MRT.** MAE en GBP, WAPE, biais, couverture des scénarios et volume de semaines ; seuils et coûts à fixer avec le métier. **Avis : PROMETTEUR** pour prévision des ventes observées, sous ce périmètre.

## PRJ3 — Olist Brazilian E-Commerce

Source : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce ; Olist, version 2. La réponse de l’API officielle conservée indique **CC BY-NC-SA 4.0**. Étude non commerciale, attribution et obligations ShareAlike applicables ; ne pas utiliser directement données/dérivés pour une prestation payante sans clarification des droits.

**Mesures.** Neuf tables. 99 441 commandes, 112 650 articles, 103 886 paiements, 99 224 avis. Achats du 2016-09-04 21:15:19 au 2018-10-17 17:30:18. Clés commandes/clients uniques ; clés composées articles/paiements uniques ; aucun orphelin commande dans articles, paiements ou avis. 551 avis supplémentaires sur des commandes déjà représentées. 261 831 répétitions exactes dans la géolocalisation : aucune jointure directe au ZIP sans agrégation.

La jointure préagrégée conserve 99 441 commandes. Une jointure naïve commandes×articles×paiements produit 117 601 lignes : les sommes seraient exposées au double comptage.

**Qualité du KPI.** 96 470 commandes livrées ont les deux dates nécessaires ; 2 971 commandes exclues du dénominateur. 6 534 livraisons après le jour promis, soit 6.77%. Ce taux est conditionnel aux commandes livrées exploitables, pas un taux de fiabilité sur toutes les commandes. Les cohortes récentes peuvent être incomplètes.

**Gate 0.** Analyste opérations : prioriser les segments à investiguer une fois les résultats de livraison connus. Pas de modèle nécessaire, de sanction automatique ni de conclusion causale. Abstention sur petits volumes. **Fuites :** statut final, livraison et avis interdits comme variables connues à l’achat. Historique de révision de la date promise inconnu.

**MRT.** Retards/commandes matures, volumes, intervalles et nombre de dossiers à examiner. Coûts d’action inconnus. **Avis : PROMETTEUR** pour diagnostic rétrospectif non commercial.

## PRJ4 — CFPB Historical Narratives Archive

Source : https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/ . Réutilisation : https://www.consumerfinance.gov/data-research/consumer-complaints/ indique que les données publiées peuvent être utilisées, analysées et servir de base à d’autres travaux. Aucune licence CC globale inventée. Récits personnels : conserver en local et ne pas republier le texte.

**Acquisition : TERMINÉ sur les 21 exports officiels.** Les premières URL copiées depuis le rendu web renvoyaient 403 ; l’extraction des liens exacts depuis la page officielle a résolu l’accès. Il ne faut pas demander de compte CFPB ou de secret. `cfpb_links.json` recense les 21 URL et `cfpb_audit.json` les fichiers contrôlés. Un échec ou un fichier incomplet reste visible et exclu des totaux.

**Gate 0.** Suggérer une grande catégorie de produit à un agent de réception, avec abstention et revue humaine ; aucune prétention à reproduire le routage institutionnel. Le label est la sélection du consommateur, pas une vérité de traitement. Les plaintes sont des allégations et ne sont pas représentatives de tous les consommateurs.

**DPD/fuites.** Auditer le texte réellement présent, la taxonomie et les doublons. Pas de réponse de l’entreprise ni de métadonnées postérieures comme entrées. Split temporel, déduplication exacte avant split et analyse des quasi-doublons nécessaires. Mots de produit explicites et modèles de lettres peuvent rendre l’évaluation artificiellement favorable. La confidentialité ne se réduit pas aux marqueurs XXXX.

**MRT.** Macro-F1, résultats par classe, couverture d’acceptation, erreurs acceptées, dossiers en revue, coût/latence si effectivement exécutés. Seuil choisi sur validation uniquement ; coûts métier inconnus. **Avis : PROMETTEUR sous réserves pour un périmètre historique de triage assisté ; validation de projet encore requise.** Banking77 n’a pas été substitué.

### Mesures CFPB par export contrôlé

| Export | Lignes | Récits non vides | Répétitions textuelles normalisées | Motifs email | Motifs téléphone |
|---|---:|---:|---:|---:|---:|
| CCDB_Export_10_March_2025_through_April_2025.zip | 803 073 | 210 147 | 117 400 | 9 | 0 |
| CCDB_Export_11_May_2025_through_June_2025.zip | 827 343 | 219 632 | 114 053 | 9 | 24 |
| CCDB_Export_12_July_2025_through_August_2025.zip | 968 761 | 234 404 | 117 329 | 6 | 44 |
| CCDB_Export_13_September_2025_through_October_2025.zip | 1 023 636 | 157 821 | 73 459 | 6 | 5 |
| CCDB_Export_14_November_2025_through_December_2025.zip | 1 009 132 | 134 641 | 59 448 | 4 | 5 |
| CCDB_Export_15_January_2026_through_February_2026.zip | 1 038 383 | 34 351 | 3 234 | 3 | 1 |
| CCDB_Export_16_March_2026.zip | 614 945 | 21 640 | 2 361 | 2 | 0 |
| CCDB_Export_17_April_2026.zip | 618 293 | 21 052 | 1 538 | 3 | 0 |
| CCDB_Export_18_May_2026.zip | 619 940 | 17 528 | 1 729 | 1 | 0 |
| CCDB_Export_19_June_2026.zip | 620 794 | 16 820 | 1 444 | 0 | 0 |
| CCDB_Export_1_December_2011_through_April_2018.zip | 1 031 863 | 291 574 | 11 561 | 31 | 3 |
| CCDB_Export_20_July_2026.zip | 672 036 | 10 002 | 623 | 0 | 0 |
| CCDB_Export_21_August_2026.zip | 667 140 | 1 | 0 | 0 | 0 |
| CCDB_Export_2_May_2018_through_April_2021.zip | 1 041 632 | 439 860 | 66 348 | 115 | 7 |
| CCDB_Export_3_May_2021_through_October_2022.zip | 977 426 | 408 046 | 89 199 | 52 | 3 |
| CCDB_Export_4_November_2022_through_August_2023.zip | 987 495 | 388 495 | 106 725 | 33 | 1 |
| CCDB_Export_5_September_2023_through_March_2024.zip | 945 532 | 318 804 | 111 044 | 17 | 1 |
| CCDB_Export_6_April_2024_through_July_2024.zip | 839 903 | 276 332 | 126 780 | 2 | 1 |
| CCDB_Export_7_August_2024_through_October_2024.zip | 824 514 | 229 944 | 105 974 | 7 | 1 |
| CCDB_Export_8_November_2024_through_December_2024.zip | 591 058 | 154 916 | 67 150 | 6 | 0 |
| CCDB_Export_9_January_2025_through_February_2025.zip | 811 019 | 265 405 | 122 772 | 8 | 1 |

Les répétitions ci-dessus sont mesurées dans chaque export, pas entre exports. Les motifs email/téléphone sont des alertes regex, ni une preuve d’identité ni un audit PII exhaustif. Les distributions par produit et les manquants sont dans le JSON.

**Synthèse du périmètre complet audité.** 3 851 415 récits non vides sur 17 533 918 lignes (21.97%). 1 300 171 occurrences au-delà de la première après minuscules et normalisation des espaces, comptées à l’intérieur de chaque export (33.76% des récits). 314 récits contiennent un motif email et 97 un motif de téléphone ; ne pas publier les textes. 0 identifiants répétés à l’intérieur des exports ; unicité entre exports non encore prouvée. Les fenêtres temporelles doivent aussi être contrôlées.

Produits les plus fréquents parmi les récits (libellés historiques conservés) :

- Credit reporting or other personal consumer reports : 1 672 429 (43.42%).
- Credit reporting, credit repair services, or other personal consumer reports : 807 499 (20.97%).
- Debt collection : 445 246 (11.56%).
- Checking or savings account : 189 350 (4.92%).
- Mortgage : 147 249 (3.82%).

**Période réelle des récits non vides : 2015-03-19 00:00:00 à 2026-08-11 00:00:00.** `cfpb_temporal.json` donne les volumes par année et produit ; ce contrôle sépare les dates des plaintes de celles des récits effectivement disponibles.

## PRJ5 — UCI MetroPT-3

Source : https://archive.ics.uci.edu/dataset/791/metropt+3+dataset ; Davari et al., DOI 10.24432/C5VW3R. Licence officielle CC BY 4.0 ; citer aussi les publications référencées par UCI.

**Mesures.** 1 516 948 observations, 15 capteurs, du 2020-02-01 00:00:00 au 2020-09-01 03:59:50. Aucun manquant dans les colonnes du CSV, aucune répétition de ligne ou d’horodatage. Cela ne signifie pas absence de trous temporels. 1 337 521 intervalles de 10 s ; 128 277 de 9 s ; 51 147 intervalles >10 s, comprenant la variation ordinaire à 11–13 s. Coupure maximale : 172 918 s. La période réelle dépasse donc la seule mention « février–août ».

**Labels.** CSV non labellisé ; quatre fenêtres de fuite d’air dans les rapports officiels. Le numéro d’événement est dupliqué et une date de maintenance paraît incohérente : conserver le texte source, ne pas inventer une correction. Une anomalie n’est pas une panne. Un signal durant la panne n’est pas une anticipation.

**Gate 0.** Analyste maintenance : examiner les régimes inhabituels persistants à la fermeture d’un bin de dix minutes, ou différer. Pas d’arrêt automatique ni de décision de sécurité. Normalisation et modèle sur février seulement ; données manquantes signalées et continuité des alertes interrompue.

**MRT.** Épisodes d’alerte, heures sous alerte, exposition observée, recouvrement de chaque événement et signaux avant début. Les alertes hors rapport sont non vérifiées, pas des faux positifs prouvés. Coût d’inspection et coût d’événement manqué inconnus. **Avis : PROMETTEUR pour étudier la fiabilité des alertes ; FAIBLE pour démontrer maintenance prédictive ou réduction des pannes.**

## Preuves disponibles et limites de revue

- Archives UCI/Olist : `acquisition.json`, bruts intacts, empreintes et CRC.
- CFPB : `cfpb_links.json`, `cfpb_access.json`, `cfpb_integrity.json`, `cfpb_audit.json` et bruts.
- Qualité : `retail_audit.json`, `olist_audit.json`, `metro_audit.json`, `cfpb_audit.json`.
- Scripts : `src/audit.py`, `src/cfpb.py --audit-only` ; environnement : `environment.json`.
- Tests : sept tests exécutés et réussis, voir `audit_tests.txt` ; exhaustivité des 21 archives, intégrité, rapprochements et régression sur le comptage des répétitions. Ces contrôles ne constituent pas une revue exhaustive de tous les risques.
- Contrats Gate 0/DPD/MRT : `docs/DECISION_CONTRACTS.md`.
- Expériences antérieures : `retail_evaluation.json`, `metro_evaluation.json` ; **exploratoires non validées**, aucune qualification de projet terminé.
- Aucune compétence personnelle autonome n’est validée. Aucune expérience client, ROI ou exploitation industrielle n’est revendiquée.

## Décisions demandées à l’orchestration

1. Valider Retail sur les ventes observées, avec sensibilité aux retours et répétitions avant production.
2. Valider Olist comme étude rétrospective non commerciale ; réserver le sujet de réutilisation commerciale.
3. Valider CFPB sur un périmètre de taxonomie stable et revue humaine, avec contrôle renforcé des templates et de la confidentialité.
4. Valider MetroPT-3 comme étude d’alertes expérimentale, avec limites explicites sur les quatre événements.
5. Confirmer la reprise de production projets/LAB seulement après cette revue ; Telco reste indépendant et attend son accès.

Plan concret : `docs/PLAN_VALIDATION.md`. Toutes les plateformes restent NON PUBLIÉ. Aucun accès supplémentaire n’est nécessaire pour les audits publics en cours.
