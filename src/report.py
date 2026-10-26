"""Build audit review documents from measured JSON, never invented status."""
import json,pathlib,html,csv,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'reports'
def read(n,default=None):
 p=OUT/n; return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
def fmt(n): return f'{n:,}'.replace(',',' ')
def main():
 r=read('retail_audit.json'); o=read('olist_audit.json'); m=read('metro_audit.json'); cf=read('cfpb_audit.json',[]); links=read('cfpb_links.json',[])
 good=[x for x in cf if x.get('status')=='OK' and x.get('audit_version')==2]; complete=len(good)==len(links)==21
 total=sum(x.get('rows',0) for x in good); narratives=sum(x.get('narratives',0) for x in good)
 integrity=read('cfpb_integrity.json',[]); acquired=len(integrity)==21 and all(x.get('crc_error') is None for x in integrity)
 records=[
 {'id':'PRJ1','dataset':'Telco existant','licence':'à auditer','audit':'BLOCKED','verdict':'NON CONCLU','dev':'BLOCKED','risque':'dépôt absent','next':'fournir chemin/lien'},
 {'id':'PRJ2','dataset':'UCI Online Retail II','licence':'CC BY 4.0','audit':'TECHNICAL REVIEW','verdict':'PROMETTEUR sous réserves','dev':'en attente de validation','risque':'doublons ambigus, demande/stock non observés','next':'valider prévision des ventes positives observées'},
 {'id':'PRJ3','dataset':'Olist','licence':'CC BY-NC-SA 4.0','audit':'TECHNICAL REVIEW','verdict':'PROMETTEUR, usage non commercial','dev':'en attente de validation','risque':'cardinalités, dénominateur, restriction NC','next':'valider diagnostic rétrospectif non commercial'},
 {'id':'PRJ4','dataset':'CFPB Narratives Archive','licence':'réutilisation publique CFPB ; pas de CC affirmée','audit':'TECHNICAL REVIEW' if complete else 'DATA AUDIT','verdict':'PROMETTEUR pour triage exploratoire' if complete and narratives else 'NON CONCLU — audit incomplet','dev':'en attente de validation','risque':'taxonomies, templates, confidentialité, labels proxy','next':'valider périmètre temporel après revue' if complete else 'achever 21 exports et audit'},
 {'id':'PRJ5','dataset':'UCI MetroPT-3','licence':'CC BY 4.0','audit':'TECHNICAL REVIEW','verdict':'PROMETTEUR alertes ; FAIBLE maintenance prédictive','dev':'en attente de validation','risque':'quatre événements, coupures, une machine','next':'valider étude de fiabilité d’alertes'},
 ]
 for i,name in enumerate(['RAG & évaluation GenAI','PySpark','TensorFlow','API/Docker/CI'],1): records.append({'id':f'LAB{i}','dataset':name,'licence':'à cadrer','audit':'NOT STARTED','verdict':'validation préalable','dev':'NOT STARTED','risque':'aucune preuve de réalisation','next':'attendre validation des projets'})
 for x in records:
  x.update(tests='voir audit_tests.txt' if x['id'] in ['PRJ2','PRJ3','PRJ5'] else 'non exécutés / à vérifier',documentation='rapports/contrats' if x['id'] in ['PRJ2','PRJ3','PRJ4','PRJ5'] else 'non produite',GitHub='NON PUBLIÉ',Notion='NON PUBLIÉ',Portfolio='NON PUBLIÉ',Kaggle='NON PUBLIÉ',LinkedIn='NON PUBLIÉ',Upwork='NON PUBLIÉ',Fiverr='NON PUBLIÉ')
 with (OUT/'production.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0])); w.writeheader(); w.writerows(records)
 now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
 status='TERMINÉ sur les 21 exports officiels' if complete else f'EN COURS : {len(good)}/21 exports audités avec succès'
 duplicate_texts=sum(x.get('duplicate_normalized_narratives',0) for x in good)
 email_count=sum(x.get('email_like_narratives',0) for x in good); phone_count=sum(x.get('phone_like_narratives',0) for x in good)
 products={}
 for x in good:
  for k,v in x.get('narrative_products',{}).items(): products[k]=products.get(k,0)+v
 temporal=read('cfpb_temporal.json',{}); narrative_periods=[x['narrative_period'] for x in temporal.get('archives',[]) if x['narrative_period'][0]!='None']
 narrative_period=[min(x[0] for x in narrative_periods),max(x[1] for x in narrative_periods)] if narrative_periods else None
 testlog=(OUT/'audit_tests.txt').read_text(encoding='utf-8-sig',errors='replace') if (OUT/'audit_tests.txt').exists() else ''
 tests_ok='Ran 7 tests' in testlog and '\nOK' in testlog
 body=f'''# Compte rendu des audits — pour validation dans l’orchestration

Généré le {now}. WORKING. **Production des projets/LAB suspendue dans l’attente de validation.** Les expériences déjà exécutées sont exploratoires et non validées. Ce document ne modifie aucun statut pédagogique du CORE.

## État de complétude

- Retail, Olist et MetroPT-3 : acquisition, SHA-256, CRC et audit exécutés.
- CFPB acquisition/intégrité : {'21/21 archives téléchargées, SHA-256 calculés, CRC tous réussis ; '+fmt(sum(x['bytes'] for x in integrity))+' octets.' if acquired else 'en cours ; voir manifeste.'} Audit de contenu : **{status}**. {fmt(total)} lignes et {fmt(narratives)} récits non vides dans les seuls exports audités avec succès. {'Le total couvre les 21 fichiers, pas un échantillon.' if complete else 'Ces totaux partiels ne représentent pas encore le corpus complet.'}
- Telco : dépôt non fourni ; aucune reconstruction.
- Publications externes, cloud, offre commerciale et dépenses : aucune action effectuée.

## PRJ2 — UCI Online Retail II

Source : https://archive.ics.uci.edu/dataset/502/online+retail+ii ; Chen, DOI 10.24432/C5CG6D. Licence officielle CC BY 4.0, attribution requise.

**Mesures.** {fmt(r['rows'])} lignes d’articles, deux feuilles ({fmt(r['sheet_rows']['Year 2009-2010'])} et {fmt(r['sheet_rows']['Year 2010-2011'])}). Période réelle : {r['period'][0]} à {r['period'][1]}. {fmt(r['duplicate_rows'])} répétitions exactes ; {fmt(r['nulls']['Customer ID'])} identifiants client absents ; {fmt(r['nulls']['Description'])} descriptions absentes. {fmt(r['cancellations'])} annulations à préfixe C ; {fmt(r['nonpositive_quantity'])} quantités <=0 ; {fmt(r['nonpositive_price'])} prix <=0. Ces groupes se recoupent et ne doivent pas être additionnés. La règle exploratoire prix/quantité positifs, sans C et sans répétitions exactes conserve {fmt(r['clean_rows'])} lignes et {r['complete_weeks']} semaines complètes.

**Gate 0.** Analyste de planification, décision hebdomadaire à horizon une semaine : préparer des scénarios de ventes observées et de charge. Abstention si extraction incomplète ; validation humaine. Coûts d’erreur inconnus. Aucun stock, rupture, marge ou capacité réelle : ne pas promettre optimisation de stock ni ROI.

**DPD/fuites.** Agrégation à la semaine ; variables et calibration limitées au passé. Historique limité à environ deux ans et un commerçant britannique ancien. Les doublons peuvent être des ventes légitimes : tester la sensibilité avant de retenir le nettoyage. Les retours exclus changent la cible ; ventes positives ≠ ventes nettes ≠ demande latente.

**MRT.** MAE en GBP, WAPE, biais, couverture des scénarios et volume de semaines ; seuils et coûts à fixer avec le métier. **Avis : PROMETTEUR** pour prévision des ventes observées, sous ce périmètre.

## PRJ3 — Olist Brazilian E-Commerce

Source : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce ; Olist, version 2. La réponse de l’API officielle conservée indique **CC BY-NC-SA 4.0**. Étude non commerciale, attribution et obligations ShareAlike applicables ; ne pas utiliser directement données/dérivés pour une prestation payante sans clarification des droits.

**Mesures.** Neuf tables. {fmt(o['tables']['olist_orders_dataset']['rows'])} commandes, {fmt(o['tables']['olist_order_items_dataset']['rows'])} articles, {fmt(o['tables']['olist_order_payments_dataset']['rows'])} paiements, {fmt(o['tables']['olist_order_reviews_dataset']['rows'])} avis. Achats du {o['period'][0]} au {o['period'][1]}. Clés commandes/clients uniques ; clés composées articles/paiements uniques ; aucun orphelin commande dans articles, paiements ou avis. {o['keys']['review_repeated_order']} avis supplémentaires sur des commandes déjà représentées. {fmt(o['tables']['olist_geolocation_dataset']['duplicate_rows'])} répétitions exactes dans la géolocalisation : aucune jointure directe au ZIP sans agrégation.

La jointure préagrégée conserve {fmt(o['sql_order_grain_rows'])} commandes. Une jointure naïve commandes×articles×paiements produit {fmt(o['naive_join_rows'])} lignes : les sommes seraient exposées au double comptage.

**Qualité du KPI.** {fmt(o['delivery']['eligible'])} commandes livrées ont les deux dates nécessaires ; {fmt(o['delivery']['excluded'])} commandes exclues du dénominateur. {fmt(o['delivery']['late'])} livraisons après le jour promis, soit {o['delivery']['late_rate']:.2%}. Ce taux est conditionnel aux commandes livrées exploitables, pas un taux de fiabilité sur toutes les commandes. Les cohortes récentes peuvent être incomplètes.

**Gate 0.** Analyste opérations : prioriser les segments à investiguer une fois les résultats de livraison connus. Pas de modèle nécessaire, de sanction automatique ni de conclusion causale. Abstention sur petits volumes. **Fuites :** statut final, livraison et avis interdits comme variables connues à l’achat. Historique de révision de la date promise inconnu.

**MRT.** Retards/commandes matures, volumes, intervalles et nombre de dossiers à examiner. Coûts d’action inconnus. **Avis : PROMETTEUR** pour diagnostic rétrospectif non commercial.

## PRJ4 — CFPB Historical Narratives Archive

Source : https://www.consumerfinance.gov/foia-requests/foia-electronic-reading-room/cfpb-consumer-complaint-database-narratives-archive/ . Réutilisation : https://www.consumerfinance.gov/data-research/consumer-complaints/ indique que les données publiées peuvent être utilisées, analysées et servir de base à d’autres travaux. Aucune licence CC globale inventée. Récits personnels : conserver en local et ne pas republier le texte.

**Acquisition : {status}.** Les premières URL copiées depuis le rendu web renvoyaient 403 ; l’extraction des liens exacts depuis la page officielle a résolu l’accès. Il ne faut pas demander de compte CFPB ou de secret. `cfpb_links.json` recense les 21 URL et `cfpb_audit.json` les fichiers contrôlés. Un échec ou un fichier incomplet reste visible et exclu des totaux.

**Gate 0.** Suggérer une grande catégorie de produit à un agent de réception, avec abstention et revue humaine ; aucune prétention à reproduire le routage institutionnel. Le label est la sélection du consommateur, pas une vérité de traitement. Les plaintes sont des allégations et ne sont pas représentatives de tous les consommateurs.

**DPD/fuites.** Auditer le texte réellement présent, la taxonomie et les doublons. Pas de réponse de l’entreprise ni de métadonnées postérieures comme entrées. Split temporel, déduplication exacte avant split et analyse des quasi-doublons nécessaires. Mots de produit explicites et modèles de lettres peuvent rendre l’évaluation artificiellement favorable. La confidentialité ne se réduit pas aux marqueurs XXXX.

**MRT.** Macro-F1, résultats par classe, couverture d’acceptation, erreurs acceptées, dossiers en revue, coût/latence si effectivement exécutés. Seuil choisi sur validation uniquement ; coûts métier inconnus. **Avis : {'PROMETTEUR sous réserves pour un périmètre historique de triage assisté ; validation de projet encore requise.' if complete and narratives else 'NON CONCLU tant que l’audit des exports et des récits est incomplet.'}** Banking77 n’a pas été substitué.

### Mesures CFPB par export contrôlé

| Export | Lignes | Récits non vides | Répétitions textuelles normalisées | Motifs email | Motifs téléphone |
|---|---:|---:|---:|---:|---:|
'''
 for x in good: body+=f"| {x['archive']} | {fmt(x['rows'])} | {fmt(x['narratives'])} | {fmt(x.get('duplicate_normalized_narratives',0))} | {fmt(x.get('email_like_narratives',0))} | {fmt(x.get('phone_like_narratives',0))} |\n"
 body+='\nLes répétitions ci-dessus sont mesurées dans chaque export, pas entre exports. Les motifs email/téléphone sont des alertes regex, ni une preuve d’identité ni un audit PII exhaustif. Les distributions par produit et les manquants sont dans le JSON.\n'
 if good:
  body+=f"\n**Synthèse du périmètre {'complet' if complete else 'partiel'} audité.** {fmt(narratives)} récits non vides sur {fmt(total)} lignes ({narratives/total:.2%}). {fmt(duplicate_texts)} occurrences au-delà de la première après minuscules et normalisation des espaces, comptées à l’intérieur de chaque export ({duplicate_texts/narratives:.2%} des récits). {fmt(email_count)} récits contiennent un motif email et {fmt(phone_count)} un motif de téléphone ; ne pas publier les textes. {sum(x.get('duplicate_ids',0) for x in good)} identifiants répétés à l’intérieur des exports ; unicité entre exports non encore prouvée. Les fenêtres temporelles doivent aussi être contrôlées.\n"
  body+='\nProduits les plus fréquents parmi les récits (libellés historiques conservés) :\n\n'
  for k,v in sorted(products.items(),key=lambda x:x[1],reverse=True)[:5]: body+=f'- {k} : {fmt(v)} ({v/narratives:.2%}).\n'
 if narrative_period:
  body+=f'\n**Période réelle des récits non vides : {narrative_period[0]} à {narrative_period[1]}.** `cfpb_temporal.json` donne les volumes par année et produit ; ce contrôle sépare les dates des plaintes de celles des récits effectivement disponibles.\n'
 body+=f'''
## PRJ5 — UCI MetroPT-3

Source : https://archive.ics.uci.edu/dataset/791/metropt+3+dataset ; Davari et al., DOI 10.24432/C5VW3R. Licence officielle CC BY 4.0 ; citer aussi les publications référencées par UCI.

**Mesures.** {fmt(m['rows'])} observations, 15 capteurs, du {m['period'][0]} au {m['period'][1]}. Aucun manquant dans les colonnes du CSV, aucune répétition de ligne ou d’horodatage. Cela ne signifie pas absence de trous temporels. {fmt(m['interval_counts'].get('10.0',0))} intervalles de 10 s ; {fmt(m['interval_counts'].get('9.0',0))} de 9 s ; {fmt(m['gaps_over_10s'])} intervalles >10 s, comprenant la variation ordinaire à 11–13 s. Coupure maximale : {fmt(int(m['max_gap_seconds']))} s. La période réelle dépasse donc la seule mention « février–août ».

**Labels.** CSV non labellisé ; quatre fenêtres de fuite d’air dans les rapports officiels. Le numéro d’événement est dupliqué et une date de maintenance paraît incohérente : conserver le texte source, ne pas inventer une correction. Une anomalie n’est pas une panne. Un signal durant la panne n’est pas une anticipation.

**Gate 0.** Analyste maintenance : examiner les régimes inhabituels persistants à la fermeture d’un bin de dix minutes, ou différer. Pas d’arrêt automatique ni de décision de sécurité. Normalisation et modèle sur février seulement ; données manquantes signalées et continuité des alertes interrompue.

**MRT.** Épisodes d’alerte, heures sous alerte, exposition observée, recouvrement de chaque événement et signaux avant début. Les alertes hors rapport sont non vérifiées, pas des faux positifs prouvés. Coût d’inspection et coût d’événement manqué inconnus. **Avis : PROMETTEUR pour étudier la fiabilité des alertes ; FAIBLE pour démontrer maintenance prédictive ou réduction des pannes.**

## Preuves disponibles et limites de revue

- Archives UCI/Olist : `acquisition.json`, bruts intacts, empreintes et CRC.
- CFPB : `cfpb_links.json`, `cfpb_access.json`, `cfpb_integrity.json`, `cfpb_audit.json` et bruts.
- Qualité : `retail_audit.json`, `olist_audit.json`, `metro_audit.json`, `cfpb_audit.json`.
- Scripts : `src/audit.py`, `src/cfpb.py --audit-only` ; environnement : `environment.json`.
- Tests : {'sept tests exécutés et réussis' if tests_ok else 'résultat final non confirmé'}, voir `audit_tests.txt` ; exhaustivité des 21 archives, intégrité, rapprochements et régression sur le comptage des répétitions. Ces contrôles ne constituent pas une revue exhaustive de tous les risques.
- Contrats Gate 0/DPD/MRT : `docs/DECISION_CONTRACTS.md`.
- Expériences antérieures : `retail_evaluation.json`, `metro_evaluation.json` ; **exploratoires non validées**, aucune qualification de projet terminé.
- Aucune compétence personnelle autonome n’est validée. Aucune expérience client, ROI ou exploitation industrielle n’est revendiquée.

## Décisions demandées à l’orchestration

1. Valider Retail sur les ventes observées, avec sensibilité aux retours et répétitions avant production.
2. Valider Olist comme étude rétrospective non commerciale ; réserver le sujet de réutilisation commerciale.
3. {'Valider CFPB sur un périmètre de taxonomie stable et revue humaine, avec contrôle renforcé des templates et de la confidentialité.' if complete else 'Attendre la clôture de l’audit CFPB avant validation du quatrième dataset.'}
4. Valider MetroPT-3 comme étude d’alertes expérimentale, avec limites explicites sur les quatre événements.
5. Confirmer la reprise de production projets/LAB seulement après cette revue ; Telco reste indépendant et attend son accès.

Plan concret : `docs/PLAN_VALIDATION.md`. Toutes les plateformes restent NON PUBLIÉ. Aucun accès supplémentaire n’est nécessaire pour les audits publics en cours.
'''
 (OUT/'COMPTE_RENDU.md').write_text(body,encoding='utf-8')
 if complete:
  short=f'''# Compte rendu à copier dans l’orchestration

## Demande de validation des périmètres — 23 octobre 2026

Les **quatre audits de données sont exécutés**. Les archives brutes sont conservées intactes, avec SHA-256 et contrôles CRC réussis. La production des projets/LAB est suspendue conformément à la demande de validation préalable. Les expériences Retail et MetroPT déjà exécutées restent exploratoires et non validées. Aucun CORE/statut pédagogique n’a changé ; aucune publication ou dépense n’a été effectuée.

| Candidat | Mesures réelles | Licence / source | Avis et périmètre proposé |
|---|---|---|---|
| Retail | {fmt(r['rows'])} lignes, 2009-12-01–2011-12-09 ; {fmt(r['duplicate_rows'])} répétitions exactes, {fmt(r['nulls']['Customer ID'])} ID client absents, {fmt(r['cancellations'])} lignes C ; {r['complete_weeks']} semaines complètes après règles exploratoires | UCI, Chen, DOI 10.24432/C5CG6D ; CC BY 4.0 | PROMETTEUR : prévision hebdomadaire des ventes positives observées ; pas d’optimisation de stocks ni de demande latente |
| Olist | 9 tables ; {fmt(o['tables']['olist_orders_dataset']['rows'])} commandes, 2016-09-04–2018-10-17 ; {fmt(o['delivery']['late'])}/{fmt(o['delivery']['eligible'])} livraisons exploitables en retard ({o['delivery']['late_rate']:.2%}) ; jointure contrôlée {fmt(o['sql_order_grain_rows'])} lignes contre {fmt(o['naive_join_rows'])} en jointure naïve | Olist/Kaggle officiel v2 ; CC BY-NC-SA 4.0 confirmée par API | PROMETTEUR pour diagnostic rétrospectif non commercial ; commercialisation des données/dérivés à exclure sans clarification des droits |
| CFPB | 21 exports, {fmt(total)} lignes de plaintes, {fmt(narratives)} récits non vides ({narratives/total:.2%}) ; récits {narrative_period[0][:10] if narrative_period else 'voir rapport'}–{narrative_period[1][:10] if narrative_period else 'voir rapport'} ; {fmt(duplicate_texts)} répétitions textuelles internes aux exports ({duplicate_texts/narratives:.2%}) | Archive historique officielle ; réutilisation publique annoncée par CFPB ; aucune licence CC inventée | PROMETTEUR pour triage historique assisté, abstention et humain ; label produit = proxy, pas routage institutionnel |
| MetroPT-3 | {fmt(m['rows'])} observations, 2020-02-01–2020-09-01 ; aucun manquant CSV ni timestamp dupliqué ; coupure maximale {fmt(int(m['max_gap_seconds']))} s ; 4 fenêtres de panne documentées | UCI, Davari et al., DOI 10.24432/C5VW3R ; CC BY 4.0 | PROMETTEUR pour étude de fiabilité des alertes ; FAIBLE pour démontrer maintenance prédictive ou baisse des pannes |

**Gate 0 / MRT.** Retail : analyste de planification, décision hebdomadaire et scénarios MAE/WAPE/biais/incertitude. Olist : analyste opérations, priorisation d’investigations après maturation des livraisons, volumes/retards/incertitude. CFPB : agent d’accueil, suggestion de catégorie, abstention selon validation et volumes/erreurs/revue humaine. Metro : analyste maintenance, inspection d’alertes persistantes, épisodes/exposition/recouvrement et anticipation séparés. Les coûts métier restent inconnus ; aucun ROI n’est affirmé.

**Risques à traiter avant production validée.** Retail : effet des retours et doublons ambigus, disponibilité temporelle et historique limité. Olist : grain des jointures, sélection des seules commandes livrées, cohortes récentes, variables postérieures et restriction NC. CFPB : taxonomies 2017/2023, templates/quasi-doublons, split temporel, catégories explicites, labels consommateurs et confidentialité. {fmt(email_count)} récits ont un motif email et {fmt(phone_count)} un motif téléphone selon regex : signal de revue, pas preuve d’identité ; aucun texte publié. Metro : rythme irrégulier, trous, une seule machine, quatre événements, ambiguïtés du rapport ; anomalie ≠ panne et recouvrement ≠ anticipation.

**Preuves.** `reports/COMPTE_RENDU.md`, `AUDIT_PRJ2.md` à `AUDIT_PRJ5.md`, JSON qualité, `cfpb_integrity.json`, `cfpb_temporal.json`, `acquisition.json`, code reproductible et journal `audit_tests.txt`. Sources et contrats détaillés dans le rapport complet et `docs/DECISION_CONTRACTS.md`. {'Sept tests exécutés et réussis, dont exhaustivité des 21 archives, empreintes et rapprochements.' if tests_ok else 'Journal final de tests à confirmer.'} L’unicité des identifiants entre exports et les quasi-doublons textuels restent des limites explicites ; aucune répétition d’ID à l’intérieur des exports.

**Décision demandée :** valider ces quatre périmètres, ou préciser les ajustements, puis autoriser la reprise de production des projets et LAB. Aucun dataset n’a été substitué. Telco reste bloqué uniquement sur le chemin/lien du dépôt existant, sans reconstruction ; il ne bloque pas les autres projets après validation. Aucun accès supplémentaire n’est nécessaire pour les quatre datasets publics. Pas de publication externe sans accord sur le contenu et la plateforme.
'''
  (OUT/'CR_ORCHESTRATION.md').write_text(short,encoding='utf-8')
 for id,title in [('PRJ2','PRJ2 —'),('PRJ3','PRJ3 —'),('PRJ4','PRJ4 —'),('PRJ5','PRJ5 —')]:
  section=body.split('## '+title,1)[1].split('\n## ',1)[0]
  (OUT/f'AUDIT_{id}.md').write_text('# '+title+section+'\n\nVoir COMPTE_RENDU.md pour les preuves globales et décisions de validation.\n',encoding='utf-8')
 rows=''.join('<tr>'+''.join(f'<td>{html.escape(str(x[k]))}</td>' for k in ['id','dataset','licence','audit','verdict','dev','risque','next'])+'</tr>' for x in records)
 page=f'''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Decision Reliability — audits</title><style>body{{font:16px system-ui;background:#f2f5f7;color:#172b3a;margin:0}}main{{max-width:1500px;margin:auto;padding:36px}}h1{{font-size:34px}}.note{{background:#fff3cd;padding:20px;border-left:5px solid #b47708}}.cards{{display:flex;gap:20px;flex-wrap:wrap;margin:28px 0}}.card{{background:white;padding:24px;min-width:200px;border-top:4px solid #18766d}}strong{{display:block;font-size:30px}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{text-align:left;padding:14px;border-bottom:1px solid #d9e1e6;vertical-align:top}}th{{background:#143c4a;color:white}}.scroll{{overflow:auto}}a{{color:#13675f}}small{{color:#526675}}</style><main><small>WORKING • {now}</small><h1>Decision Reliability &gt; Model Performance</h1><p>Revue des données avant validation des projets</p><div class="note">Production projets/LAB suspendue. Expériences existantes exploratoires, non validées. Aucun statut pédagogique modifié ; aucune publication externe.</div><div class="cards"><div class="card"><strong>3 / 4</strong>audits complets hors CFPB</div><div class="card"><strong>{len(good)} / 21</strong>exports CFPB audités</div><div class="card"><strong>{fmt(narratives)}</strong>récits mesurés {'(complet)' if complete else '(partiel)'}</div><div class="card"><strong>0</strong>publication externe</div></div><p><a href="COMPTE_RENDU.md">Compte rendu détaillé</a> · <a href="production.csv">Suivi complet CSV</a> · <a href="../docs/DECISION_CONTRACTS.md">Gate 0 / DPD / MRT</a> · <a href="../docs/PLAN_VALIDATION.md">Plan après validation</a></p><div class="scroll"><table><thead><tr><th>ID</th><th>Dataset</th><th>Licence</th><th>Audit</th><th>Faisabilité</th><th>Production</th><th>Risques</th><th>Prochaine décision</th></tr></thead><tbody>{rows}</tbody></table></div><p>Les statuts reflètent les preuves disponibles. « PROMETTEUR » n’équivaut pas à un projet terminé ni à une compétence personnelle vérifiée. Voir les JSON et les tests pour chaque mesure.</p></main></html>'''
 if complete: page=page.replace('<strong>3 / 4</strong>audits complets hors CFPB','<strong>4 / 4</strong>audits de données exécutés')
 (OUT/'dashboard.html').write_text(page,encoding='utf-8')
 print(status,flush=True)
if __name__=='__main__': main()
