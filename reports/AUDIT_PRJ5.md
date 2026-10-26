# PRJ5 — UCI MetroPT-3

Source : https://archive.ics.uci.edu/dataset/791/metropt+3+dataset ; Davari et al., DOI 10.24432/C5VW3R. Licence officielle CC BY 4.0 ; citer aussi les publications référencées par UCI.

**Mesures.** 1 516 948 observations, 15 capteurs, du 2020-02-01 00:00:00 au 2020-09-01 03:59:50. Aucun manquant dans les colonnes du CSV, aucune répétition de ligne ou d’horodatage. Cela ne signifie pas absence de trous temporels. 1 337 521 intervalles de 10 s ; 128 277 de 9 s ; 51 147 intervalles >10 s, comprenant la variation ordinaire à 11–13 s. Coupure maximale : 172 918 s. La période réelle dépasse donc la seule mention « février–août ».

**Labels.** CSV non labellisé ; quatre fenêtres de fuite d’air dans les rapports officiels. Le numéro d’événement est dupliqué et une date de maintenance paraît incohérente : conserver le texte source, ne pas inventer une correction. Une anomalie n’est pas une panne. Un signal durant la panne n’est pas une anticipation.

**Gate 0.** Analyste maintenance : examiner les régimes inhabituels persistants à la fermeture d’un bin de dix minutes, ou différer. Pas d’arrêt automatique ni de décision de sécurité. Normalisation et modèle sur février seulement ; données manquantes signalées et continuité des alertes interrompue.

**MRT.** Épisodes d’alerte, heures sous alerte, exposition observée, recouvrement de chaque événement et signaux avant début. Les alertes hors rapport sont non vérifiées, pas des faux positifs prouvés. Coût d’inspection et coût d’événement manqué inconnus. **Avis : PROMETTEUR pour étudier la fiabilité des alertes ; FAIBLE pour démontrer maintenance prédictive ou réduction des pannes.**


Voir COMPTE_RENDU.md pour les preuves globales et décisions de validation.
