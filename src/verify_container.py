import subprocess,json,time,pathlib,urllib.request,urllib.error,hashlib,os,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'projects/LAB4_delivery/results';DOCKER=os.environ.get('DFDS_DOCKER') or shutil.which('docker') or str(pathlib.Path(os.environ.get('LOCALAPPDATA',''))/'Programs/DockerDesktop/resources/bin/docker.exe');NAME='dfds-lab4-review'
def cli(*args):return subprocess.check_output([DOCKER,*args],text=True,encoding='utf-8').strip()
def request(path,body=None):
 data=json.dumps(body).encode() if body is not None else None
 req=urllib.request.Request('http://127.0.0.1:18765'+path,data=data,headers={'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=5) as r:return r.status,json.load(r),r.headers.get('X-Request-ID')
 except urllib.error.HTTPError as e:return e.code,json.load(e),e.headers.get('X-Request-ID')
def main():
 proof={'image':'dfds-lab4:review','engine':json.loads(cli('version','--format','{{json .}}')),'image_inspect':json.loads(cli('image','inspect','dfds-lab4:review'))[0]['Id'],'listener':'127.0.0.1:18765','fixtures':'synthetic numeric only','cloud':'NOT DEPLOYED','remote_ci':'NOT EXECUTED'}
 cid=cli('run','-d','--name',NAME,'-p','127.0.0.1:18765:8000','--health-interval=2s','dfds-lab4:review');proof['container_id']=cid
 try:
  for _ in range(30):
   try:
    h=request('/health');break
   except (OSError,ValueError):time.sleep(1)
  else:raise RuntimeError('HTTP startup timeout')
  assert h[0]==200 and h[1]['status']=='ok' and h[2]
  f=request('/forecast',{'weekly_sales':list(range(1,105))});assert f[0]==200 and f[1]['forecast']==53 and f[2]
  checks=[]
  for label,body in [('short',{'weekly_sales':[1]*51}),('negative',{'weekly_sales':[-1]*52}),('over_bound',{'weekly_sales':[1e11]*52}),('null',{'weekly_sales':[None]*52}),('nonfinite',{'weekly_sales':[float('nan')]*52})]:
   x=request('/forecast',body);assert x[0]==422,(label,x);checks.append({'case':label,'http':x[0],'request_id_present':bool(x[2])})
  for _ in range(20):
   state=json.loads(cli('inspect',NAME))[0]
   if state['State']['Health']['Status']=='healthy':break
   time.sleep(1)
  assert state['State']['Health']['Status']=='healthy'
  assert state['HostConfig']['PortBindings']['8000/tcp'][0]['HostIp']=='127.0.0.1'
  uid=cli('exec',NAME,'id','-u');assert uid!='0'
  proof.update(verified=True,health_http=h[0],forecast_http=f[0],forecast=f[1]['forecast'],invalid_cases=checks,request_id_header=True,healthcheck=state['State']['Health'],nonroot_uid=uid,port_bindings=state['HostConfig']['PortBindings'])
 finally:
  cli('stop',NAME);st=json.loads(cli('inspect',NAME))[0]['State'];proof['stopped']=not st['Running'];proof['exit_code']=st['ExitCode'];proof['verified']=bool(proof.get('verified') and proof['stopped'] and proof['exit_code']==0);logs=subprocess.run([DOCKER,'logs',NAME],capture_output=True,text=True);(OUT/'container_run.txt').write_text(logs.stdout+logs.stderr,encoding='utf-8');proof['logs_saved']='container_run.txt'
  (OUT/'container_smoke.json').write_text(json.dumps(proof,indent=2),encoding='utf-8')
 assert proof['stopped'] and proof['exit_code']==0
 print(json.dumps({'health':proof['health_http'],'forecast':proof['forecast'],'invalid_cases':len(checks),'healthcheck':'healthy','uid':uid,'stopped':proof['stopped']}))
if __name__=='__main__':main()
