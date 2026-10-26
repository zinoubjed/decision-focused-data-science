"""Compare substantive measured outcomes, not hardware-dependent timings."""
import argparse,json,pathlib,math,hashlib
from common import ROOT,save
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--reproduced-root',required=True);args=ap.parse_args();other=pathlib.Path(args.reproduced_root);checks=[]
 def read(base,folder,file='metrics.json'):return json.loads((base/'projects'/folder/'results'/file).read_text())
 def compare(name,a,b,tolerance=1e-10):
  equal=math.isclose(a,b,rel_tol=tolerance,abs_tol=tolerance) if isinstance(a,(int,float)) and isinstance(b,(int,float)) else a==b
  checks.append({'check':name,'reference':a,'reproduced':b,'matches':equal});assert equal,name
 r=read(ROOT,'PRJ2_retail');s=read(other,'PRJ2_retail');compare('retail selected model',r['variants'][r['primary']]['selected_on_validation'],s['variants'][s['primary']]['selected_on_validation'])
 for f in ['MAE','WAPE']:compare('retail '+f,r['variants'][r['primary']]['seasonal_52'][f],s['variants'][s['primary']]['seasonal_52'][f])
 compare('retail interval coverage',r['variants'][r['primary']]['interval']['test_coverage'],s['variants'][s['primary']]['interval']['test_coverage'])
 for folder,keys in [('PRJ3_olist',['grain_rows','mature_rate','late_rate_delivered_only']),('PRJ4_cfpb',['training','validation','test','selected_model','test_macro_f1','accepted','accepted_wrong','human_review']),('LAB2_pyspark',['input_rows','parquet_roundtrip','null_required','output_month_rows']),('LAB4_delivery',['health_http','forecast_http','invalid_input_http','example_forecast'])]:
  a,b=read(ROOT,folder),read(other,folder)
  for k in keys:compare(folder+' '+k,a[k],b[k])
 a,b=read(ROOT,'PRJ5_metro'),read(other,'PRJ5_metro')
 for x,y in zip(a['results'],b['results']):compare('metro '+x['model']+' '+str(x['training_quantile'])+' episodes',x['episodes'],y['episodes'])
 for k in ['baseline_correct','raw_rag_correct','guarded_correct','reference_document_precision']:compare('rag '+k,read(ROOT,'LAB1_rag','scoring_v2.json')[k],read(other,'LAB1_rag','scoring_v2.json')[k])
 a,b=read(ROOT,'LAB3_tensorflow'),read(other,'LAB3_tensorflow');compare('tensorflow selection',a['retained'],b['retained']);compare('tensorflow baseline',a['baseline']['test_accuracy'],b['baseline']['test_accuracy'])
 for x,y in zip(a['tensorflow_runs'],b['tensorflow_runs']):compare('tensorflow seed '+str(x['seed']),x['test_accuracy'],y['test_accuracy'],tolerance=.006) # <= about 2 digits on the same small held-out set
 for k in ['llm_accuracy','tfidf_accuracy_same_subset']:compare('local LLM diagnostic '+k,read(ROOT,'PRJ4_cfpb','local_llm_diagnostic.json')[k],read(other,'PRJ4_cfpb','local_llm_diagnostic.json')[k])
 source_differences=[]
 for p in (other/'src').glob('*.py'):
  current=ROOT/'src'/p.name
  if current.exists() and p.read_bytes()!=current.read_bytes():source_differences.append(p.name)
 save(ROOT/'reports/isolated_comparison.json',{'checks':checks,'matches':all(x['matches'] for x in checks),'comparison_scope':'Substantive counts/model choices/errors. Hardware timings excluded; TensorFlow accuracy tolerance .006 across CPU reruns.','code_snapshot_differences_after_extraction':source_differences,'snapshot_scope_note':'Final documentation/editorial packaging and bounded helper/logging edits may follow extraction; differences are listed, not represented as identical final-archive execution.'})
 print('Substantive reproduction comparisons passed:',len(checks),'snapshot differences:',source_differences,flush=True)
if __name__=='__main__':main()
