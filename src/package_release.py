"""Create a private review archive by allowlist, excluding all data and runtimes."""
import pathlib,json,hashlib,zipfile,re
from html.parser import HTMLParser
from common import ROOT,save
PUBLIC_RESULTS={
 'PRJ1_telco':{'audit.json','source_integrity.json','metrics.json'},
 'LAB1_rag':{'metrics.json','corpus_manifest.json','evaluation_rows.json','semantic_review.json','scoring_v2.json','scored_rows_v2.json','rubric_v2.json'},
 'LAB2_pyspark':{'metrics.json','monthly_sensor_stats.csv'},
 'LAB3_tensorflow':{'metrics.json','learning_history.csv'},
 'LAB4_delivery':{'metrics.json','blocker.json','docker_installation.json','container_smoke.json','container_run.txt','container_build.txt'},
 'PRJ2_retail':{'metrics.json','sql_check.json','backtest_remove_exact_duplicates.csv','backtest_retain_ambiguous_duplicates.csv','weekly_remove_exact_duplicates.csv','weekly_retain_ambiguous_duplicates.csv','predictions_with_intervals_remove_exact_duplicates.csv','predictions_with_intervals_retain_ambiguous_duplicates.csv','error_by_month.csv'},
 'PRJ3_olist':{'metrics.json','cohorts.csv','dashboard.html','relational_review.json','state_investigation.csv'},
 'PRJ4_cfpb':{'metrics.json','confusion.csv','decision_population.json','error_summary.json','local_llm_confusion.csv','local_llm_diagnostic.json','selective_by_actual_class.json'},
 'PRJ5_metro':{'metrics.json','episodes.csv','scores.csv'}}
PUBLIC_REPORTS=set('acquisition.json acquisition_refresh.json cfpb_access.json cfpb_audit.json cfpb_integrity.json cfpb_links.json cfpb_temporal.json companion_notebook_execution.json COMPTE_RENDU.md CR_ORCHESTRATION.md critical_review_tests.txt post_docker_tests.txt dashboard.html environment_incidents.json environment.json final_tests.txt java_manifest.json lab_runtime_freeze.txt metro_10min.csv metro_audit.json metro_evaluation.json model_manifest.json olist_audit.json olist_delivery_by_state.csv olist_delivery_month.csv olist_metadata.json production_current.csv production_current.json production_unit_tests.txt production.csv resume_integrity_tests.txt retail_audit.json retail_evaluation.json retail_predictions.csv retail_weekly.csv spark_critical_review.txt spark_execution.txt spark_fs_manifest.json tensorflow_bootstrap.json audit_tests.txt isolated_reproduction.json isolated_comparison.json coverage_review.json'.split())|{f'AUDIT_PRJ{i}.md' for i in range(2,6)}|{f'isolated_{s}.py.txt' for s in ['retail_production','cfpb_production','review_cfpb','lab_spark','lab_tensorflow','lab_rag']}
def permitted_artifact(relative):
 rel=pathlib.Path(relative);parts=rel.parts
 if any(p in {'data','.runtime','.venv','.git','history','__pycache__'} for p in parts):return False
 if len(parts)==1:return rel.name in {'README.md','ATTRIBUTIONS.md','PRODUCTION_STATUS.md','production.html','Dockerfile','.gitignore','.dockerignore','requirements-core.txt','requirements-core-lock.txt','requirements-labs.txt','requirements-lab-base.txt','requirements-editorial.txt'}
 if parts[0] in {'src','tests'}:return rel.suffix=='.py'
 if parts[0]=='reports':return len(parts)==2 and rel.name in PUBLIC_REPORTS
 if parts[0]=='docs':return rel.suffix=='.md'
 if parts[0]=='.github':return rel.as_posix()=='.github/workflows/ci.yml'
 if parts[0]=='projects' and len(parts)>=3 and parts[1] in PUBLIC_RESULTS:
  if len(parts)==3:return rel.name in {'README.md','aggregation.sql','order_grain.sql','transform.sql','evidence_companion.ipynb'}
  if parts[2]=='results':return len(parts)==4 and rel.name in PUBLIC_RESULTS[parts[1]]
  if parts[2]=='docs':return rel.suffix=='.md'
  if parts[2]=='figures':return rel.suffix=='.png'
  if parts[1]=='LAB1_rag' and parts[2]=='corpus':return rel.suffix=='.txt'
 return False
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if (tag=='a' and k=='href') or (tag=='img' and k=='src'):self.urls.append(v)
def main():
 notebook_checks=[]
 for path in sorted((ROOT/'projects').glob('*/evidence_companion.ipynb')):
  nb=json.loads(path.read_text(encoding='utf-8'));case=path.parent;meta=nb['metadata'];assert meta.get('preparation_version')==2,'Outdated notebook preparation'
  assert meta['evidence_metrics_sha256']==hashlib.sha256((case/'results/metrics.json').read_bytes()).hexdigest(),'Notebook metrics changed after execution'
  for name,sha in meta.get('supplement_sha256',{}).items():assert sha==hashlib.sha256((case/'results'/name).read_bytes()).hexdigest(),'Notebook supplementary evidence changed'
  figure=next(iter((case/'figures').glob('*.png')),None) if (case/'figures').exists() else None
  assert meta.get('evidence_figure_sha256')==(hashlib.sha256(figure.read_bytes()).hexdigest() if figure else None)
  code=[c for c in nb['cells'] if c['cell_type']=='code'];assert all(c.get('execution_count') is not None and not any(o.get('output_type')=='error' for o in c.get('outputs',[])) for c in code),'Unexecuted/error notebook cell'
  notebook_checks.append({'notebook':str(path.relative_to(ROOT)),'executed_cells':len(code),'asset_hashes_match':True})
 assert len(notebook_checks)==7,'Seven completed companion notebooks required for release'
 # Validate the current showcase and actual local dashboard links before archiving.
 checked=[]
 for p in [ROOT/'production.html',ROOT/'projects/PRJ3_olist/results/dashboard.html']:
  parser=Links();parser.feed(p.read_text(encoding='utf-8'))
  for url in parser.urls:
   if url.startswith(('https://','http://','#')):continue
   dest=(p.parent/url.split('#')[0]).resolve();assert dest.is_relative_to(ROOT.resolve()) and dest.exists(),(p,url)
   checked.append({'page':str(p.relative_to(ROOT)),'target':url})
 files=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(ROOT)
  if not permitted_artifact(rel):continue
  if any(x in ['data','__pycache__','.venv','.git','.runtime','history'] for x in rel.parts):continue
  if p.suffix in ['.log','.pyc','.part','.joblib','.parquet','.safetensors']:continue
  if p.name.endswith('_source_page.html'):continue
  if p.name in ['release_manifest.json','release_validation.json']:continue
  if rel.parts[0]=='reports' and (len(rel.parts)!=2 or p.name not in PUBLIC_REPORTS):continue
  if rel.parts[0]=='projects' and 'results' in rel.parts and p.name not in PUBLIC_RESULTS.get(rel.parts[1],set()):continue
  if p.suffix.lower() not in ['.md','.py','.sql','.json','.csv','.txt','.html','.png','.yml','.ipynb'] and p.name not in ['Dockerfile','.gitignore','.dockerignore']:continue
  files.append((p,rel))
 assert not any('data' in rel.parts for p,rel in files)
 records=[{'path':str(rel).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest()} for p,rel in files]
 manifest={'purpose':'Private review package; NOT an external publication or commercial license grant','raw_or_private_data_included':False,'public_derived_evidence_included':True,'runtime_or_model_weights_included':False,'results_policy':'Explicit allowed result/report filenames; unknown files are not auto-released. Public UCI aggregates and noncommercial Olist derivatives included with attribution; no CFPB narrative or vocabulary.','files':records}
 save(ROOT/'reports/release_manifest.json',manifest)
 output=ROOT.parent/'portfolio_release_draft.zip'
 with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for p,rel in files:z.write(p,'portfolio/'+str(rel).replace('\\','/'))
  z.write(ROOT/'reports/release_manifest.json','portfolio/reports/release_manifest.json')
 with zipfile.ZipFile(output) as z:
  assert z.testzip() is None
  assert not any('/data/' in n or n.endswith(('.joblib','.parquet','.safetensors')) for n in z.namelist())
 validation={'local_links_checked':len(checked),'broken_links':0,'notebook_checks':notebook_checks,'archive':output.name,'bytes':output.stat().st_size,'sha256':hashlib.file_digest(output.open('rb'),'sha256').hexdigest(),'crc_error':None,'file_count':len(files)+1,'excluded':'Raw/private data, complaint texts/IDs/vocabulary/model bundles, runtimes, weights, historical ZIPs; public aggregates/derived evidence are intentionally included','remaining_blockers':['Exact external publication/platform approval']}
 save(ROOT/'reports/release_validation.json',validation);print(validation,flush=True)
if __name__=='__main__':main()
