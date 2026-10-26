# PRJ3 — Olist Brazilian E-Commerce

Source : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce ; Olist, version 2. La réponse de l’API officielle conservée indique **CC BY-NC-SA 4.0**. Étude non commerciale, attribution et obligations ShareAlike applicables ; ne pas utiliser directement données/dérivés pour une prestation payante sans clarification des droits.

**Mesures.** Neuf tables. 99 441 commandes, 112 650 articles, 103 886 paiements, 99 224 avis. Achats du 2016-09-04 21:15:19 au 2018-10-17 17:30:18. Clés commandes/clients uniques ; clés composées articles/paiements uniques ; aucun orphelin commande dans articles, paiements ou avis. 551 avis supplémentaires sur des commandes déjà représentées. 261 831 répétitions exactes dans la géolocalisation : aucune jointure directe au ZIP sans agrégation.

La jointure préagrégée conserve 99 441 commandes. Une jointure naïve commandes×articles×paiements produit 117 601 lignes : les sommes seraient exposées au double comptage.

**Qualité du KPI.** 96 470 commandes livrées ont les deux dates nécessaires ; 2 971 commandes exclues du dénominateur. 6 534 livraisons après le jour promis, soit 6.77%. Ce taux est conditionnel aux commandes livrées exploitables, pas un taux de fiabilité sur toutes les commandes. Les cohortes récentes peuvent être incomplètes.

**Gate 0.** Analyste opérations : prioriser les segments à investiguer une fois les résultats de livraison connus. Pas de modèle nécessaire, de sanction automatique ni de conclusion causale. Abstention sur petits volumes. **Fuites :** statut final, livraison et avis interdits comme variables connues à l’achat. Historique de révision de la date promise inconnu.

**MRT.** Retards/commandes matures, volumes, intervalles et nombre de dossiers à examiner. Coûts d’action inconnus. **Avis : PROMETTEUR** pour diagnostic rétrospectif non commercial.


Voir COMPTE_RENDU.md pour les preuves globales et décisions de validation.
