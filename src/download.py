"""Fetch official sources without overwriting acquired bytes."""
import concurrent.futures, hashlib, json, pathlib, datetime, urllib.request, re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def expected_hashes():
 expected={}
 for record in json.loads((ROOT/'reports/acquisition.json').read_text()):
  if record.get('status')=='OK':expected[record['name']+'.zip']=record['sha256']
 for record in json.loads((ROOT/'reports/cfpb_integrity.json').read_text()):expected[record['file']]=record['sha256']
 return expected
SOURCES={
 'retail': 'https://archive.ics.uci.edu/static/public/502/online%2Bretail%2Bii.zip',
 'metro': 'https://archive.ics.uci.edu/static/public/791/metropt%2B3%2Bdataset.zip',
 'olist': 'https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce',
}
def fetch(item):
 name,url=item; p=ROOT/'data/raw'/f'{name}.zip'
 record={'name':name,'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  if not p.exists():
   req=urllib.request.Request(url,headers={'User-Agent':'DecisionReliabilityPortfolio/1.0'})
   with urllib.request.urlopen(req,timeout=180) as r, p.with_suffix('.part').open('wb') as f:
    record['content_type']=r.headers.get('Content-Type')
    while chunk:=r.read(1024*1024): f.write(chunk)
   p.with_suffix('.part').rename(p)
  with p.open('rb') as f: record['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
  if record['sha256']!=expected_hashes().get(p.name):raise ValueError('Archive differs from frozen audit fingerprint; preserved for investigation, not silently accepted')
  record['bytes']=p.stat().st_size
  import zipfile
  with zipfile.ZipFile(p) as z: record['members']=z.namelist(); record['crc_error']=z.testzip()
  record['status']='OK'
 except Exception as e: record.update(status='FAILED',error=str(e))
 print(json.dumps(record),flush=True)
 return record
if __name__=='__main__':
 (ROOT/'data/raw').mkdir(parents=True,exist_ok=True)
 (ROOT/'reports').mkdir(exist_ok=True)
 # Reproduce the dated corpus, not an unannounced newer live archive catalog.
 links=json.loads((ROOT/'reports/cfpb_links.json').read_text())
 for url in links: SOURCES[url.rsplit('/',1)[-1].removesuffix('.zip')]=url
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(fetch,SOURCES.items()))
 (ROOT/'reports/acquisition_refresh.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 if any(r['status']!='OK' for r in results):raise SystemExit('Acquisition incomplete or fingerprint mismatch; see acquisition_refresh.json')
