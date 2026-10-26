"""Evidence-derived editorial artifacts. No publishing, no personal-skill claims."""
import json,pathlib,html,csv,datetime,argparse
from common import ROOT,save
CONFIG={
 'PRJ2_retail':('PRJ2','Retail Sales Forecasting & Operational Planning','retail_production.py','UCI Online Retail II; Chen; DOI 10.24432/C5CG6D; CC BY 4.0','Planning analyst reviews next week’s positive observed sales and uncertainty. No inventory, margin or latent-demand inference.'),
 'PRJ3_olist':('PRJ3','E-commerce Delivery Reliability Analytics','olist_production.py','Olist official Kaggle v2; CC BY-NC-SA 4.0; noncommercial only','Operations analyst prioritises delivery segments for investigation after outcomes mature. No purchase-time prediction or causal sanction.'),
 'PRJ4_cfpb':('PRJ4','Financial Complaint Triage & LLM Evaluation','cfpb_production.py','CFPB official Historical Narratives Archive; public reuse statement, no blanket CC assertion','Assist intake staff with consumer-product suggestions, abstention and human review. Product selection is a proxy, not institutional routing ground truth.'),
 'PRJ5_metro':('PRJ5','Industrial Anomaly Detection & Alert Reliability','metro_production.py','UCI MetroPT-3; Davari et al.; DOI 10.24432/C5VW3R; CC BY 4.0','Maintenance analyst reviews persistent unusual regimes. No automated safety action, downtime-reduction or operational maintenance claim.'),
 'LAB1_rag':('LAB1','RAG & Local Generative AI Evaluation','lab_rag.py','Authored fictional Lumen Library policies; corpus CC0-1.0; FLAN-T5-small Apache-2.0','Evaluate source retrieval, local generation, abstention and failure modes on a fixed diagnostic set. Not a production knowledge assistant.'),
 'LAB2_pyspark':('LAB2','PySpark Sensor Data Engineering','lab_spark.py','UCI MetroPT-3, CC BY 4.0, Davari et al.; PySpark Apache-2.0','Verify typed distributed transformations, Spark SQL and Parquet against pandas on one local machine.'),
 'LAB3_tensorflow':('LAB3','TensorFlow vs Classical Baseline Benchmark','lab_tensorflow.py','scikit-learn bundled UCI optical digits; cite original creators E. Alpaydin and C. Kaynak and sklearn load_digits; no images redistributed','Test a CPU Keras MLP against logistic regression; retain complexity only when validation supports it.'),
 'LAB4_delivery':('LAB4','Local API, Docker & CI Delivery','lab_api.py','Authored numeric API and synthetic test fixtures; no private data or model weights in image','Deliver a finite-input numeric baseline API, test rejection paths, prepare container and CI, document rollback. Cloud not deployed.')}
def load(p):return json.loads(p.read_text()) if p.exists() else None
def evidence(folder,m):
 if not m:return 'Execution incomplete; see blocker record.','No measured completion claim is made.'
 if folder=='PRJ2_retail':
  v=m['variants'][m['primary']];sel=v['selected_on_validation'];test=v[sel];other=m['variants']['remove_exact_duplicates']['seasonal_52'];return f"Validation selected {sel}. On {test['n']} held-out one-week origins: MAE £{test['MAE']:,.2f}, WAPE {test['WAPE']:.2%}, signed bias £{test['bias_actual_minus_forecast']:,.2f}. Separate interval evaluation: {v['interval']['test_coverage']:.2%} coverage on {v['interval'].get('evaluation_weeks',26)} weeks. Exact-dedup seasonal WAPE {other['WAPE']:.2%} is a sensitivity, not a reason to alter the target.", 'Thirteen selection weeks; 26 point-forecast test weeks split into 13 calibration and 13 interval-evaluation weeks. The nominal 90% scenario fails to achieve that coverage; no 90% reliability guarantee. Annual history is short and duplicates ambiguous. Mean-4 is better on this test, but no test-driven model switch is made. Costs are hypothetical.'
 if folder=='PRJ3_olist':return f"SQL retained {m['grain_rows']:,} unique orders. All-period late rate is {m['late_all_dates']:,}/{m['eligible_all_dates']:,} = {m['late_rate_delivered_only']:.2%}, conditional on eligible delivered orders. Mature 60-day cohort rate: {m['mature_rate']:.2%}.",'Noncommercial Olist restriction. Undelivered orders are outside the late-rate denominator and explicitly counted. Export date is not known; latest purchase is a proxy, with 30/60/90-day maturity sensitivities. Wilson intervals assume independent Bernoulli outcomes; repeat-customer/route dependence and confounding remain.'
 if folder=='PRJ4_cfpb':
  flow=load(ROOT/'projects/PRJ4_cfpb/results/decision_population.json');whole=f" Overall sampled workflow: {flow['accepted_suggestions']:,}/{flow['sampled_test_before_text_filter']:,} suggestions accepted ({flow['acceptance_fraction_over_all_sampled_test']:.2%}); {flow['total_manual_review_if_duplicate_gate_is_deployed']:,} assigned to review including withheld text repeats." if flow else ''
  return f"Selected {m['selected_model']} on validation macro-F1. Novel temporal test n={m['test']:,}: accuracy {m['test_accuracy']:.2%}, macro-F1 {m['test_macro_f1']:.3f}, majority accuracy {m['majority_accuracy']:.2%}. Threshold {m['threshold']} has {m['accepted_wrong']:,} wrong accepted suggestions; {m['human_review']:,} low-confidence novel cases require review."+whole,'No automatic routing recommended: aggregate accepted accuracy hides weak true-class outcomes. Results are on a 3% ID sample and template-filtered cohort. Character matching is not semantic deduplication. Confidence/Wilson search does not give a post-selection probability guarantee. Private text and vocabulary excluded; human-verification workflow required.'
 if folder=='PRJ5_metro':
  x=next(x for x in m['results'] if x['model']=='isolation_forest' and x['training_quantile']==.995);b=next(x for x in m['results'] if x['model']=='robust_max_deviation' and x['training_quantile']==.995);hits=sum(y['alert_during_event'] for y in x['event_windows']);pre=sum(y['alert_prior_24h'] for y in x['event_windows']);return f"At training quantile .995: IsolationForest {x['episodes']} episodes versus robust baseline {b['episodes']}; {x['episodes_no_overlap_report']} IF episodes do not overlap reports. Overlap in {hits}/4 report windows; prior-24h alerts in {pre}/4. Valid exposure {x['observed_days_equivalent']:.2f} equivalent days.",'One compressor and four documented windows. No full false-positive ground truth: outside-report episodes are unverified. Threshold grid is a sensitivity, not test tuning. Bins need >=54 observations and are available at closing time; 3-bin persistence. Prior alerts may be unrelated; no causal precursor or maintenance benefit claim.'
 if folder=='LAB1_rag':
  rubric=load(ROOT/'projects/LAB1_rag/results/scoring_v2.json')
  summary=f"Local FLAN-T5-small, {m['questions']} fixed questions. Explicit post-run rubric v2: raw RAG {rubric['raw_rag_accuracy']:.0%}, guarded {rubric['guarded_accuracy']:.0%}, no-RAG {rubric['baseline_accuracy']:.0%}; reference-document precision {rubric['reference_document_precision']:.2%}. Original substring baseline score 0% is preserved but is not the semantic headline." if rubric else 'Scoring review pending.'
  return summary,'Tiny authored set, post-run rubric clarification, no blind human evaluation. Document matches are not citation entailment. The guard still accepts irrelevant copied phrases. 7-D SVD vectors are latent-semantic, not neural. Zero API charge excludes hardware/electricity. Not suitable for unattended use.'
 if folder=='LAB2_pyspark':return f"Spark {m['engine_version']}, {m['master']}: {m['input_rows']:,} sensor rows, {m['output_month_rows']} monthly aggregates. Spark Parquet roundtrip and pandas parity passed at tolerance {m['pandas_parity_tolerance']}. Elapsed {m['elapsed_seconds']:.2f}s.",'Local scale only. Timezone setting is computational normalization of naive timestamps, not evidence of original UTC. Monthly aggregation has only eight output rows; two files are sufficient and directory partitioning adds no value.'
 if folder=='LAB3_tensorflow':return f"Held-out digits test: logistic accuracy {m['baseline']['test_accuracy']:.2%}; TensorFlow seed accuracies {', '.join(format(x['test_accuracy'],'.2%') for x in m['tensorflow_runs'])}. Retained by validation complexity rule: {m['retained']}.",'Small 8×8-image benchmark, not an industrial task. Split is stratified by image, not writer-disjoint; writer dependence cannot be excluded. Three initialisation seeds share one test set. CPU timings are environment-specific; reduced Windows runtime omits only custom-op C++ headers.'
 return ('Local unit/ASGI and HTTP tests passed. Actual Docker image build, loopback health/forecast/rejection, healthcheck and stop verified.' if (load(ROOT/'projects/LAB4_delivery/results/container_smoke.json') or {}).get('verified') else 'Local unit/ASGI and HTTP tests passed. Docker Desktop installed; engine/container verification pending.'),'Remote GitHub Actions and cloud deployment are not executed. Numeric synthetic fixtures only; no public endpoint or operational benefit claim.'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--reviewed',action='store_true');args=ap.parse_args();rows=[];cards=[];root_summary=[]
 for folder,(id,title,script,license,decision) in CONFIG.items():
  p=ROOT/'projects'/folder;p.mkdir(exist_ok=True);(p/'docs').mkdir(exist_ok=True);m=load(p/'results/metrics.json');block=load(p/'results/blocker.json');summary,limits=evidence(folder,m)
  status='BLOCKED' if block else ('PUBLICATION PACKAGE READY' if args.reviewed and m else ('TECHNICAL REVIEW' if m else 'DEVELOPMENT'))
  if id=='LAB4':status='LOCAL CONTAINER VERIFIED' if (load(p/'results/container_smoke.json') or {}).get('verified') else 'BLOCKED'
  commands=f'python src/{script}'
  if id=='LAB4':commands='python -m unittest tests.test_api_ci -v\npython -m uvicorn lab_api:app --app-dir src --host 127.0.0.1 --port 8000'
  text=f'''# {title}

**{id} · {status} · portfolio project / local technical demonstration**

## Executive summary

{summary}

## Decision and scope

{decision} Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

{license}. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/{script}`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
{commands}
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

{limits}

Next action: {'resolve the documented environment blocker and run the missing checks' if block else 'review the prepared publication content, rights and personal presentation before any external release'}.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** {title}: evidence of method selection, data contracts, validation and transparent limits. {summary}

**Client-facing method summary.** {('Noncommercial case study only. Describe grain, joins, cohort definitions and quality checks without redistributing Olist-derived metrics, visuals or data into commercial offers.' if id=='PRJ3' else 'Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.')}

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
'''
  (p/'README.md').write_text(text,encoding='utf-8')
  if id=='PRJ4':
   diagnostic=load(p/'results/local_llm_diagnostic.json')
   if diagnostic:
    with (p/'README.md').open('a',encoding='utf-8') as f:f.write(f"\n## Local LLM diagnostic, not model selection\n\nOn the fixed balanced 54-case diagnostic, local FLAN-T5-small accuracy was {diagnostic['llm_accuracy']:.2%}; TF-IDF on the same cases was {diagnostic['tfidf_accuracy_same_subset']:.2%}. All inference remained local; no complaint prompts or outputs were exported. See results/local_llm_diagnostic.json. This result does not estimate full-population accuracy.\n")
  if block:limits+=' Blocker: '+block['reason']
  kit=f'''# Publication kit — draft, NOT PUBLISHED

## GitHub

Repository title: `{folder.lower().replace('_','-')}`

Lead: {decision}

Evidence: {summary}

Include executable source, tests, environment lock, attribution, limitations and AI disclosure. Exclude `data/`, credentials, private vocabularies, raw complaint text and local model weights. No repository URL exists until a repository is actually created and approved.

## Notion case study

Title: {title} — from data quality to a defensible review decision.

Structure: decision owner → available information → data promise → baseline → measured result → failure modes → action/refusal. Lead with the denominator, split or alert exposure that changes interpretation. {summary}

## Personal portfolio card

{title}. {decision} Read the reproducible evidence and limits before interpreting the result as business value. Portfolio study, AI-assisted; autonomous personal proficiency unverified.

## LinkedIn draft

One lesson from this portfolio study: the evaluation boundary changes the conclusion.

{summary}

The limit I would keep visible: {limits}

This is an AI-assisted portfolio experiment, not a client deployment or measured commercial outcome. Publication wording must be personally reviewed before use.

## Kaggle

{'Not applicable to the delivery API. Do not force a notebook platform onto an API lifecycle demonstration.' if id=='LAB4' else 'Prepare a minimal notebook invoking the documented pipeline; reference the official source and preserve licence terms. Publish only approved aggregates/code and reproducible conclusions. Do not upload raw CFPB text or private artifacts.'}

## Upwork — method-only draft

Proposed presentation topic: reliable data preparation and clearly bounded analysis. Explain scope, input contract, checks, outputs and review handoff. No pricing, guaranteed outcome, availability or service offering is authorised by this draft.

## Fiverr — method-only draft

Possible service description structure, subject to personal acceptance: specify input files and volume, output format, quality checks, revision scope and exclusions. Do not claim expertise or sell a gig automatically.

{('**Olist restriction:** For Upwork, Fiverr or any commercial context, omit Olist-derived numbers, screenshots and datasets. Use only an original general description of SQL/cardinality methodology. Noncommercial sharing must preserve attribution and applicable ShareAlike terms; public use still needs approval.' if id=='PRJ3' else '')}

## Release checklist

User approves exact platform and content; remove placeholder links; confirm attribution, private-data exclusion and personally accepted claims; attach actual run evidence. No fake client, review, deployment or outcome.
'''
  (p/'docs/PUBLICATION_KIT.md').write_text(kit,encoding='utf-8')
  rows.append({'id':id,'project':title,'status':status,'source_license':license,'execution':'metrics.json present' if m else 'not completed','tests':'see local journals and assertions','results':summary,'limits':limits,'documentation':f'projects/{folder}/README.md','reproducibility':'docs/REPRODUCIBILITY.md','package':'prepared draft','GitHub':'NOT PUBLISHED','Notion':'NOT PUBLISHED','Portfolio':'NOT PUBLISHED','Kaggle':'NOT PUBLISHED','LinkedIn':'NOT PUBLISHED','Upwork':'NOT PUBLISHED','Fiverr':'NOT PUBLISHED','next':'resolve blocker' if block else 'content approval before publication'})
  fig=next(iter((p/'figures').glob('*.png')),None) if (p/'figures').exists() else None
  image=f'<img alt="{html.escape(title)} measured result" src="{fig.relative_to(ROOT).as_posix()}">' if fig else ''
  cards.append(f'<article><span class="status">{status}</span><h2>{id} · {html.escape(title)}</h2><p>{html.escape(summary)}</p>{image}<details><summary>Limits and evidence</summary><p>{html.escape(limits)}</p><a href="projects/{folder}/README.md">Case study</a> · <a href="projects/{folder}/results/metrics.json">Measured results</a> · <a href="projects/{folder}/docs/PUBLICATION_KIT.md">Publication draft</a></details></article>')
  root_summary.append(f'| {id} | {status} | {summary} | {limits} |')
 audit=load(ROOT/'projects/PRJ1_telco/results/audit.json')
 missing={k:'' for k in rows[0]}
 if audit:
  missing.update(id='PRJ1',project='Existing Telco Churn',status='EXISTING PROJECT REPRODUCED',source_license='IBM pinned educational source; original repository root code licence absent',execution='Original locked environment, analysis, notebook and dashboard generation reproduced',tests='3 original tests; 9 executed notebook cells; five CSV comparisons',results='Test AUC 0.8433; top30 423 contacts, 246 observed churners, FP177/FN128',limits='No campaign benefit, ROI, scoring-time validity or personal mastery established',documentation='projects/PRJ1_telco/README.md',reproducibility='projects/PRJ1_telco/results/audit.json',package='Aggregate audit evidence only; original code not redistributed',next='Owner licence decision and operational validation before reuse')
  for name in ['GitHub','Notion','Portfolio','Kaggle','LinkedIn','Upwork','Fiverr']:missing[name]='EXISTING READ ONLY' if name in ['GitHub','Notion'] else 'NOT MODIFIED'
  root_summary.insert(0,'| PRJ1 | EXISTING PROJECT REPRODUCED | Test AUC .8433; top30 423/246; original analysis, 3 tests and 9 notebook cells reproduced | No campaign benefit or deployment claim |')
  cards.insert(0,'<article><span class="status">EXISTING PROJECT REPRODUCED</span><h2>PRJ1 · Existing Telco Churn</h2><p>Original analysis, three tests and nine notebook cells reproduced. Test AUC .8433; top30: 423 contacts, 246 observed churners. No demonstrated campaign benefit.</p><a href="projects/PRJ1_telco/README.md">Existing project audit</a></article>')
 else:
  missing.update(id='PRJ1',project='Existing Telco Churn',status='BLOCKED',limits='Existing repository audit evidence missing')
 rows.insert(0,missing)
 with (ROOT/'reports/production_current.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 save(ROOT/'reports/production_current.json',rows)
 (ROOT/'PRODUCTION_STATUS.md').write_text('# Production evidence — WORKING\n\nAuthorised resumption: 23 October 2026. CORE unchanged. PRJ1 Telco existing repository reproduced; see its audit evidence.\n\n| Item | Technical state | Measured evidence | Limits |\n|---|---|---|---|\n'+'\n'.join(root_summary)+'\n\nNo external publication, cost-bearing cloud service or personal skill validation. Publication packages remain drafts pending exact platform/content approval. Original audit snapshots are preserved in reports/.\n',encoding='utf-8')
 now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
 (ROOT/'production.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Decision-Focused Data Science Portfolio</title><style>body{{margin:0;background:#eef3f5;color:#143240;font:16px/1.6 system-ui}}header,main,footer{{max-width:1150px;margin:auto;padding:36px}}header{{padding-top:60px}}h1{{font-size:clamp(30px,4vw,50px);line-height:1.15;max-width:900px}}.signature{{color:#18796f;font-size:23px}}.note{{border-left:4px solid #c18b27;background:#fff5df;padding:18px}}article{{background:white;border:1px solid #d4e0e4;border-radius:12px;padding:28px;margin:25px 0}}img{{max-width:100%;height:auto}}.status{{font-size:12px;letter-spacing:.08em;color:#13766e;font-weight:700}}a{{color:#116f71}}details{{border-top:1px solid #ddd;padding-top:16px}}small{{color:#52707e}}</style><header><small>WORKING · AI-assisted portfolio · {now}</small><h1>Decision-Focused Data Scientist<br>Interpretable ML · Reliable Analytics</h1><p class="signature">From imperfect data to defensible decisions.</p><p>Data contracts, baselines, temporal validation, abstention and operational limits, backed by executable evidence.</p><div class="note">Portfolio projects and local technical demonstrations. Personal autonomous proficiency is unverified. No new external publication. Existing Telco repository and Notion pages audited read only. Docker build and remote deployment require their own evidence.</div><p><a href="PRODUCTION_STATUS.md">Evidence register</a> · <a href="reports/production_current.csv">Production tracker</a> · <a href="docs/REPRODUCIBILITY.md">Reproduce</a> · <a href="docs/AI_PROVENANCE.md">AI role</a></p></header><main>{''.join(cards)}</main><footer>Decision Reliability &gt; Model Performance. No invented ROI, client history, cloud deployment or mastery claims.</footer></html>''',encoding='utf-8')
 print('publication drafts and evidence board generated',flush=True)
 # Channel copy is a separate concrete artifact rather than an instruction outline.
 from prepare_publication import main as prepare_copy
 import sys
 original=sys.argv;sys.argv=[original[0]]
 try:prepare_copy()
 finally:sys.argv=original
if __name__=='__main__':main()
