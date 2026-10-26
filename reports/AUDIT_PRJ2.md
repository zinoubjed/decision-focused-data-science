# PRJ2 — UCI Online Retail II

Source : https://archive.ics.uci.edu/dataset/502/online+retail+ii ; Chen, DOI 10.24432/C5CG6D. Licence officielle CC BY 4.0, attribution requise.

**Mesures.** 1 067 371 lignes d’articles, deux feuilles (525 461 et 541 910). Période réelle : 2009-12-01 07:45:00 à 2011-12-09 12:50:00. 34 335 répétitions exactes ; 243 007 identifiants client absents ; 4 382 descriptions absentes. 19 494 annulations à préfixe C ; 22 950 quantités <=0 ; 6 207 prix <=0. Ces groupes se recoupent et ne doivent pas être additionnés. La règle exploratoire prix/quantité positifs, sans C et sans répétitions exactes conserve 1 007 913 lignes et 104 semaines complètes.

**Gate 0.** Analyste de planification, décision hebdomadaire à horizon une semaine : préparer des scénarios de ventes observées et de charge. Abstention si extraction incomplète ; validation humaine. Coûts d’erreur inconnus. Aucun stock, rupture, marge ou capacité réelle : ne pas promettre optimisation de stock ni ROI.

**DPD/fuites.** Agrégation à la semaine ; variables et calibration limitées au passé. Historique limité à environ deux ans et un commerçant britannique ancien. Les doublons peuvent être des ventes légitimes : tester la sensibilité avant de retenir le nettoyage. Les retours exclus changent la cible ; ventes positives ≠ ventes nettes ≠ demande latente.

**MRT.** MAE en GBP, WAPE, biais, couverture des scénarios et volume de semaines ; seuils et coûts à fixer avec le métier. **Avis : PROMETTEUR** pour prévision des ventes observées, sous ce périmètre.


Voir COMPTE_RENDU.md pour les preuves globales et décisions de validation.
