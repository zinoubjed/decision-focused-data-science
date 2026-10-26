"""Portable orchestration of real computations, using two explicit environments.
Does not install software, download data by default, publish or provision services.
"""
import argparse,os,pathlib,subprocess,json,datetime,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--core-python',required=True);ap.add_argument('--lab-python',required=True);ap.add_argument('--assets',required=True);ap.add_argument('--core-site');ap.add_argument('--include-download-check',action='store_true');args=ap.parse_args()
 proof=ROOT/'reports/reproduction_run';proof.mkdir(exist_ok=True);records=[]
 core=[('retail_production.py',[]),('olist_production.py',[]),('cfpb_production.py',[]),('review_cfpb.py',[]),('review_olist.py',[]),('metro_production.py',[]),('lab_api_smoke.py',[])]
 labs=[('fetch_runtime_assets.py',['--offline']),('lab_rag.py',[]),('lab_spark.py',[]),('lab_tensorflow.py',[]),('cfpb_local_llm.py',[])]
 if args.include_download_check:core.insert(0,('download.py',[]))
 for group,python,steps in [('core',args.core_python,core),('labs',args.lab_python,labs)]:
  env=os.environ.copy();env['DFDS_WORK_DIR']=str(pathlib.Path(args.assets).resolve());env['MPLCONFIGDIR']=str(pathlib.Path(args.assets).resolve()/'plot-cache');env.pop('PYTHONPATH',None)
  if group=='core' and args.core_site:env['PYTHONPATH']=str(pathlib.Path(args.core_site).resolve())
  if group=='labs':
   env['PYSPARK_PYTHON']=str(pathlib.Path(python).resolve());homes=list((pathlib.Path(args.assets)/'java17').glob('*/bin/java.exe'))
   if homes:env['JAVA_HOME']=str(homes[0].parent.parent);env['PATH']=str(homes[0].parent)+os.pathsep+env['PATH']
  for script,extra in steps:
   start=datetime.datetime.now(datetime.timezone.utc).isoformat();path=proof/(script+'.txt');print('RUN',group,script,flush=True)
   with path.open('w',encoding='utf-8') as log:result=subprocess.run([python,str(ROOT/'src'/script),*extra],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
   records.append({'group':group,'script':script,'script_sha256':hashlib.sha256((ROOT/'src'/script).read_bytes()).hexdigest(),'common_sha256':hashlib.sha256((ROOT/'src/common.py').read_bytes()).hexdigest(),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':result.returncode,'log':str(path.relative_to(ROOT))})
   (ROOT/'reports/reproduction_run.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
   if result.returncode:raise SystemExit(f'Failed {script}; inspect {path}')
 print(f'All {len(records)} production commands completed; Docker and remote CI are not claimed.',flush=True)
if __name__=='__main__':main()
