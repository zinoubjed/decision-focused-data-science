# Decision-Focused Data Science

**Zaineb Mhiri · Decision-Focused Data Scientist | Interpretable ML | Reliable Analytics**

*From imperfect data to defensible decisions.*

Neuf études et laboratoires assistés par IA, présentés autour de décisions, de contrôles de données, de références simples et de limites vérifiables. Les résultats proviennent d’exécutions locales documentées ; ils ne valident pas une maîtrise personnelle autonome, une expérience client ou un usage en production.

## Parcours de lecture

Commencer par **Retail** pour le choix du modèle et l’incertitude, **Olist** pour la fiabilité des indicateurs SQL, puis **CFPB** pour l’abstention et la revue humaine. Les quatre laboratoires apportent des preuves d’exécution RAG local, Spark, TensorFlow et Docker. Le projet Telco existant a été reproduit sans reconstruction.

| Réalisation | Résultat vérifié | Limite et décision |

|---|---|---|

| [PRJ1 Telco](projects/PRJ1_telco/README.md) | Dépôt existant figé, 29 fichiers vérifiés ; environnement original neuf, 3 tests, 9 cellules notebook ; cinq CSV et résumé concordants. AUC test 0,8433 ; top30 : 423 contacts, 246 départs observés. Deux pages Notion cohérentes. | Classement historique éducatif ; aucun client sauvé ou bénéfice de campagne démontré. Validation opérationnelle et choix de licence du code encore nécessaires. |

| [PRJ2 Retail](projects/PRJ2_retail/README.md) | Baseline saisonnière choisie avant test ; WAPE 17,40 % sur 26 semaines ; sensibilité déduplication 14,34 %. SQL réconcilié. | Ventes positives observées ; ni demande latente ni stock. Couverture 61,54 % sur 13 semaines d’évaluation : le scénario nominal 90 % échoue empiriquement. |

| [PRJ3 Olist](projects/PRJ3_olist/README.md) | 99 441 commandes conservées au bon grain ; 6 534 retards sur 96 470 livraisons éligibles, soit 6,77 % ; cohorte mature 6,85 %. | Dénominateur conditionnel ; pas de causalité. Licence non commerciale : présentation commerciale limitée à la méthode. |

| [PRJ4 CFPB](projects/PRJ4_cfpb/README.md) | Échantillon déterministe 3 %, séparation temporelle et contrôle des répétitions ; précision globale test 80,74 %, macro-F1 0,632. File complète : 5 047 dossiers sur 8 218 en revue humaine. | STOP au routage automatique : faibles résultats des classes rares. Suggestions vérifiées par une personne ; textes, vocabulaire et modèle privés exclus de l’archive. |

| [PRJ5 MetroPT](projects/PRJ5_metro/README.md) | IsolationForest : 30 épisodes contre 175 pour la référence robuste ; recouvrement 4/4 fenêtres documentées, anticipation 24 h seulement 1/4. | Une machine et quatre fenêtres ; alertes hors rapports non vérifiées. Aucun gain de maintenance ou usage de sécurité démontré. |

| [LAB1 RAG local](projects/LAB1_rag/README.md) | FLAN-T5 local réel ; 20 questions fixes, grille explicite après exécution : sans RAG 10 %, brut 70 %, gardé 85 %. | Petit diagnostic ; vérification de citation mécanique, pas de preuve sémantique indépendante ni assistant autonome fiable. |

| [LAB2 PySpark](projects/LAB2_pyspark/README.md) | Spark réel sur 1 516 948 observations ; SQL, écriture/lecture Parquet et parité pandas à 1e-10. | Exécution locale, pas de cluster de production. |

| [LAB3 TensorFlow](projects/LAB3_tensorflow/README.md) | Trois entraînements réels ; exactitudes test 97,22 %, 96,67 %, 96,94 %, contre 96,39 % pour la régression logistique. | Régression logistique conservée par la règle de complexité sur validation ; petit benchmark, pas d’usage industriel. |

| [LAB4 API/Docker](projects/LAB4_delivery/README.md) | Docker Desktop 4.96.3, WSL 3.0.3, moteur 29.9.2 ; image construite et exécutée. Santé/prévision 200, prévision 53 ; cinq rejets 422, healthcheck sain, UID1000, arrêt code0. | Défaut NaN trouvé puis corrigé/testé. Écoute limitée à 127.0.0.1 ; CI distante et cloud non exécutés. |

## Vérification et reproduction

- [33 tests locaux réussis](reports/post_docker_tests.txt), dont le contrôle d’une réponse de validation NaN : correction puis essais Docker réels. Les journaux publics masquent les chemins machine ; les mesures sont conservées.
- [Reproduction de 13 commandes et 40 comparaisons](reports/isolated_comparison.json), en réutilisant les environnements existants. Ce snapshot précède la correction API, vérifiée séparément.
- Sept notebooks compagnons ont été exécutés localement ; ils lisent les preuves et figures, sans prétendre refaire l’entraînement sur Kaggle. Telco a séparément passé trois tests et neuf cellules de calcul dans son environnement original neuf.
- [Procédure de reproduction](docs/REPRODUCTION_RUNBOOK.md) · [Contrats de décision](docs/DECISION_CONTRACTS.md) · [Rôle de l’IA](docs/AI_PROVENANCE.md) · [Code](src/) · [Tests](tests/).

Les données brutes, récits et identifiants CFPB, vocabulaires/modèles privés, poids et runtimes sont exclus. Les calculs complets nécessitent les sources officielles et les environnements documentés. La suite complète exige aussi les sorties locales générées ; le dépôt seul ne contient pas tous les caches privés nécessaires. Aucun secret ni reçu de transfert privé ne fait partie de cette édition publique.

Le conteneur LAB4 a été construit, testé sur 127.0.0.1 et arrêté proprement. **GitHub Actions reste désactivé ; CI distante et cloud non exécutés.** Aucun bénéfice de campagne, ROI, gain de maintenance ou décision de sécurité n’est démontré.

## Licence et sources

**MIT couvre uniquement le code original** des sources/tests, requêtes SQL, Dockerfile et workflow, selon [LICENSING.md](LICENSING.md) et [LICENSE](LICENSE). Les résultats, données dérivées, figures, prose et éléments tiers ne sont pas couverts par cette licence de code.

**Olist : CC BY-NC-SA 4.0, usage non commercial et ShareAlike.** [Notice et transformations](projects/PRJ3_olist/DERIVATIVE_LICENSE.md). Pour une présentation commerciale, utiliser seulement la méthode générique, sans chiffres, figures, captures ou dérivés Olist. [Attributions et droits propres aux sources](ATTRIBUTIONS.md). Le code Telco original est lié, sans copie ni relicence.

## État de cette édition

Édition publique préparée le 26 octobre 2026 à partir des preuves revues le 23 octobre. Les métriques n’ont pas été recalculées pour la publication. Les anciens documents techniques et journaux sont des snapshots datés ; leurs mentions de brouillon ou d’accès privé ne décrivent pas le statut de diffusion actuel. Le suivi à jour est [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md).
