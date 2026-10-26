# PRJ4 — CFPB Historical Narratives Archive

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


Voir COMPTE_RENDU.md pour les preuves globales et décisions de validation.
