"""Real loopback HTTP smoke, automatic shutdown; no public listener."""
import subprocess,sys,time,urllib.request,urllib.error,json,os
from common import ROOT,project,save,environment
P=project('LAB4_delivery')
def main():
 log=(P/'results/local_http.log').open('w',encoding='utf-8')
 proc=subprocess.Popen([sys.executable,'-m','uvicorn','lab_api:app','--app-dir',str(ROOT/'src'),'--host','127.0.0.1','--port','18764'],stdout=log,stderr=subprocess.STDOUT,env=os.environ.copy())
 try:
  health=None
  for _ in range(40):
   try:
    with urllib.request.urlopen('http://127.0.0.1:18764/health',timeout=2) as r:health=json.load(r)
    break
   except (OSError,urllib.error.URLError):time.sleep(.25)
  assert health and health['status']=='ok'
  req=urllib.request.Request('http://127.0.0.1:18764/forecast',data=json.dumps({'weekly_sales':list(range(1,105))}).encode(),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=5) as r:answer=json.load(r);request_id=r.headers.get('X-Request-ID')
  assert answer['forecast']==53 and request_id
  bad=urllib.request.Request('http://127.0.0.1:18764/forecast',data=json.dumps({'weekly_sales':[-1]*52}).encode(),headers={'Content-Type':'application/json'})
  try:urllib.request.urlopen(bad,timeout=5);raise AssertionError('invalid input accepted')
  except urllib.error.HTTPError as e:assert e.code==422
  save(P/'results/metrics.json',{'health_http':200,'forecast_http':200,'invalid_input_http':422,'example_forecast':answer['forecast'],'listener':'127.0.0.1:18764','public_listener':False,'request_id_header':True,'test_data':'synthetic numeric values only','process_stop':'terminated in finally after smoke','docker_build':'NOT EXECUTED: engine absent','remote_ci':'NOT EXECUTED','cloud':'NOT DEPLOYED','environment':environment()})
  save(P/'results/blocker.json',{'reason':'No docker command in PATH and no executable at C:/Program Files/Docker/Docker/resources/bin/docker.exe. A running Docker engine is needed to build/run the prepared image.','completed':['unit/ASGI tests','real local HTTP health, forecast and invalid-input rejection','Dockerfile and CI config','stop/rollback documentation'],'required_action':'provide a local authorised Docker engine; no secret in chat','not_claimed':['container build/run','GitHub Actions execution','cloud deployment']});print('LAB4 real loopback HTTP passed; Docker blocked',flush=True)
 finally:
  proc.terminate()
  try:proc.wait(timeout=5)
  except subprocess.TimeoutExpired:proc.kill();proc.wait()
  log.close()
if __name__=='__main__':main()
