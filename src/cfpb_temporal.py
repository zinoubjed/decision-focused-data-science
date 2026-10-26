"""Supplemental narrative availability by year; no raw text exported."""
import pathlib,json,zipfile,pandas as pd
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 counts={}; periods=[]; records=[]
 for p in sorted((ROOT/'data/raw').glob('CCDB*.zip')):
  years={}; first=None; last=None
  with zipfile.ZipFile(p) as z:
   for n in z.namelist():
    if not n.endswith('.csv'):continue
    for d in pd.read_csv(z.open(n),usecols=['Date received','Product','Consumer complaint narrative'],chunksize=100000,dtype=str):
     d=d[d['Consumer complaint narrative'].fillna('').str.strip().str.len().gt(0)]
     t=pd.to_datetime(d['Date received'],errors='coerce')
     if t.notna().any():
      first=t.min() if first is None else min(first,t.min()); last=t.max() if last is None else max(last,t.max())
     for y,v in t.dt.year.value_counts().items():years[str(int(y))]=years.get(str(int(y)),0)+int(v)
     for (year,product),num in d.groupby([t.dt.year,'Product']).size().items():
      key=(str(int(year)),product); counts[key]=counts.get(key,0)+int(num)
  records.append({'archive':p.name,'narrative_period':[str(first),str(last)],'narratives_by_year':years})
  print('temporal',p.name,flush=True)
 out={'archives':records,'year_product':[{'year':y,'product':pr,'narratives':n} for (y,pr),n in sorted(counts.items())]}
 (ROOT/'reports/cfpb_temporal.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
if __name__=='__main__':main()
