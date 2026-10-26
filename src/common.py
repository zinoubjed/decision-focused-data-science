"""Shared local project utilities; no network calls."""
from pathlib import Path
import json,zipfile,time,platform,importlib.metadata,os
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
WORK=Path(os.environ.get('DFDS_WORK_DIR',str(ROOT/'.runtime'))).resolve()
def project(identifier):
 p=ROOT/'projects'/identifier;p.mkdir(parents=True,exist_ok=True)
 for n in ['results','docs','figures']: (p/n).mkdir(exist_ok=True)
 return p
def save(path,obj):path.write_text(json.dumps(obj,indent=2,default=str,allow_nan=False),encoding='utf-8')
def table(archive,member):
 with zipfile.ZipFile(ROOT/'data/raw'/archive) as z:return pd.read_csv(z.open(member),dtype={'customer_zip_code_prefix':'string','seller_zip_code_prefix':'string','geolocation_zip_code_prefix':'string'})
def wilson(k,n,z=1.96):
 if n<=0:return (None,None)
 p=k/n;den=1+z*z/n;mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
 return (max(0.,float(mid-half)),min(1.,float(mid+half)))
def metrics(y,p):
 e=np.asarray(y)-np.asarray(p)
 return {'n':len(e),'MAE':float(np.abs(e).mean()),'WAPE':float(np.abs(e).sum()/np.abs(y).sum()),'bias_actual_minus_forecast':float(e.mean())}
def environment():
 pkgs={}
 for p in ['pandas','numpy','scikit-learn','tensorflow','torch','transformers','pyspark','fastapi','matplotlib']:
  try:pkgs[p]=importlib.metadata.version(p)
  except importlib.metadata.PackageNotFoundError:pass
 return {'python':platform.python_version(),'platform':platform.platform(),'packages':pkgs}
def configure_plot():
 import os
 cache=WORK/'plot-cache';cache.mkdir(parents=True,exist_ok=True)
 os.environ.setdefault('MPLCONFIGDIR',str(cache))
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'figure.figsize':(10,5),'axes.spines.top':False,'axes.spines.right':False,'font.size':11,'savefig.bbox':'tight'})
 return plt
