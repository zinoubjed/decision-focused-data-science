"""Fetch pinned public assets from preserved manifests. No corpus upload or system install."""
import argparse,hashlib,json,pathlib,urllib.request,zipfile
from common import ROOT,WORK
def obtain(url,path,sha,offline):
 path.parent.mkdir(parents=True,exist_ok=True)
 if not path.exists():
  if offline:raise FileNotFoundError(path)
  with urllib.request.urlopen(url,timeout=180) as r,path.with_suffix(path.suffix+'.part').open('wb') as f:
   while chunk:=r.read(1048576):f.write(chunk)
  path.with_suffix(path.suffix+'.part').rename(path)
 with path.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
 if actual!=sha:raise ValueError(f'Asset fingerprint mismatch, preserved for investigation: {path.name}')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--offline',action='store_true');args=ap.parse_args()
 model=json.loads((ROOT/'reports/model_manifest.json').read_text())
 for name,sha in model['files'].items():obtain(f'https://huggingface.co/{model["model"]}/resolve/{model["revision"]}/{name}',WORK/'flan-t5-small'/name,sha,args.offline)
 jar=json.loads((ROOT/'reports/spark_fs_manifest.json').read_text());obtain(jar['url'],WORK/'jars/hadoop-bare-naked-local-fs-0.1.0.jar',jar['sha256'],args.offline)
 java=json.loads((ROOT/'reports/java_manifest.json').read_text())['binary']['package'];p=WORK/'java17.zip';obtain(java['link'],p,java['checksum'],args.offline)
 out=WORK/'java17';out.mkdir(exist_ok=True)
 with zipfile.ZipFile(p) as z:
  for item in z.infolist():
   dest=(out/item.filename).resolve()
   if not dest.is_relative_to(out.resolve()):raise ValueError('Unsafe Java archive path')
   if not dest.exists():z.extract(item,out)
 print('Pinned model, Java and Spark adapter verified at',WORK,flush=True)
if __name__=='__main__':main()
