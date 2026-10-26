"""Streaming archive audit and bounded historical triage experiment.
No narrative text is exported to reports. Labels are consumer product selections.
"""
import pathlib,zipfile,json,hashlib,pandas as pd,numpy as np,re,time,sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,f1_score
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'reports'
AUDIT_ONLY='--exploratory-model' not in sys.argv
def repeated_count(values,seen):
 """Number beyond first occurrence across chunks; each occurrence counted once."""
 unique=set(values); count=len(values)-len(unique-seen); seen.update(unique); return count
def main():
 files=sorted((ROOT/'data/raw').glob('CCDB*.zip')); audit=[]; samples=[]
 cache={x['archive']:x for x in json.loads((OUT/'cfpb_audit.json').read_text())} if (OUT/'cfpb_audit.json').exists() else {}
 for p in files:
  rec={'archive':p.name,'bytes':p.stat().st_size}
  with p.open('rb') as f: rec['sha256']=hashlib.file_digest(f,'sha256').hexdigest()
  old=cache.get(p.name,{})
  if AUDIT_ONLY and old.get('sha256')==rec['sha256'] and old.get('audit_version')==2 and old.get('status')=='OK':
   audit.append(old); print(p.name,'cached',flush=True); continue
  try:
   with zipfile.ZipFile(p) as z:
    rec['crc_error']=z.testzip(); rec['members']=z.namelist()
    frames=[]
    for n in z.namelist():
     if n.lower().endswith('.csv'):
      rows=0; nonempty=0; missing={}; products={}; seen_ids=set(); repeated_ids=0; start=None; end=None; text_hashes=set(); duplicate_texts=0; email_like=0; phone_like=0; empty_labels=0; invalid_dates=0; lengths=[]; narrative_products={}
      for d in pd.read_csv(z.open(n),chunksize=100000,low_memory=False):
       if rows==0: rec['columns']=list(d.columns)
       rows+=len(d)
       for c,v in d.isna().sum().items(): missing[c]=missing.get(c,0)+int(v)
       textcol=next(c for c in d if 'narrative' in c.lower()); datecol=next(c for c in d if c.lower()=='date received'); labelcol=next(c for c in d if c.lower()=='product'); idcol=next(c for c in d if c.lower()=='complaint id')
       dates=pd.to_datetime(d[datecol],errors='coerce'); invalid_dates+=int(dates.isna().sum()); a=dates.min(); b=dates.max(); start=a if start is None else min(start,a); end=b if end is None else max(end,b)
       ids=d[idcol].astype(str); repeated_ids+=repeated_count(ids,seen_ids)
       for k,v in d[labelcol].value_counts().items(): products[k]=products.get(k,0)+int(v)
       mask=d[textcol].fillna('').str.strip().str.len().gt(0); nonempty+=int(mask.sum())
       texts=d.loc[mask,textcol].astype(str); empty_labels+=int(d.loc[mask,labelcol].isna().sum())
       for k,v in d.loc[mask,labelcol].value_counts().items(): narrative_products[k]=narrative_products.get(k,0)+int(v)
       hashes=texts.str.lower().str.replace(r'\s+',' ',regex=True).map(lambda x:hashlib.sha256(x.encode()).digest())
       duplicate_texts+=repeated_count(hashes,text_hashes)
       # Filter literal @ first: avoids quadratic regex scanning on long no-email texts.
       at=texts.str.contains('@',regex=False)
       email_like+=int(texts[at].str.contains(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',regex=True).sum())
       phone_like+=int(texts.str.contains(r'\b\d{3}[-. ]\d{3}[-. ]\d{4}\b',regex=True).sum())
       lengths.extend(texts.str.len().tolist())
       if AUDIT_ONLY: continue
       sub=pd.DataFrame({'text':d.loc[mask,textcol],'date':dates[mask],'label':d.loc[mask,labelcol],'id':ids[mask]})
       # Stable ID hash sample is bounded, independent of row ordering and target.
       bucket=sub.id.map(lambda x:int(hashlib.sha256(x.encode()).hexdigest()[:8],16)%100)
       frames.append(sub[bucket<3])
      rec.update(rows=rows,narratives=nonempty,nulls=missing,products=products,narrative_products=narrative_products,period=[str(start),str(end)],duplicate_ids=repeated_ids,duplicate_normalized_narratives=duplicate_texts,email_like_narratives=email_like,phone_like_narratives=phone_like,narratives_missing_product=empty_labels,invalid_dates=invalid_dates,narrative_length_quantiles=dict(zip(['min','p50','p95','max'],map(float,np.quantile(lengths,[0,.5,.95,1])))) if lengths else {})
      samples.extend(frames)
   rec['status']='OK'; rec['audit_version']=2
  except Exception as e: rec.update(status='FAILED',error=str(e))
  audit.append(rec); print(p.name,rec.get('rows'),rec.get('narratives'),flush=True)
  (OUT/'cfpb_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 (OUT/'cfpb_audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
 if AUDIT_ONLY or not samples: return
 d=pd.concat(samples,ignore_index=True).dropna().drop_duplicates('id').sort_values('date')
 d['hash']=d.text.str.lower().str.replace(r'\s+',' ',regex=True).map(lambda x:hashlib.sha256(x.encode()).hexdigest())
 duplicates=int(d.hash.duplicated().sum()); d=d.drop_duplicates('hash',keep='first')
 # Stable taxonomy window (2018 onward, before August 2023 taxonomy change).
 d=d[(d.date>='2018-05-01')&(d.date<'2023-08-01')]
 train=d[d.date<'2022-01-01']; val=d[(d.date>='2022-01-01')&(d.date<'2023-01-01')]; test=d[d.date>='2023-01-01']
 labels=train.label.value_counts(); keep=labels[labels>=100].index
 train=train[train.label.isin(keep)]; val=val[val.label.isin(keep)]; test=test[test.label.isin(keep)]
 if min(len(train),len(val),len(test))<20:
  (OUT/'cfpb_evaluation.json').write_text(json.dumps({'status':'BLOCKED','reason':'insufficient acquired narratives in fixed taxonomy window','sample_rows':len(d)})); return
 vec=TfidfVectorizer(min_df=3,max_features=30000,ngram_range=(1,2),sublinear_tf=True,strip_accents='unicode'); X=vec.fit_transform(train.text); V=vec.transform(val.text); T=vec.transform(test.text)
 model=LogisticRegression(max_iter=500,C=1).fit(X,train.label); pred=model.predict(T); prob=model.predict_proba(T); confidence=prob.max(axis=1)
 vp=model.predict_proba(V); vc=vp.max(axis=1); vy=model.classes_[vp.argmax(axis=1)]
 choices=[]
 for threshold in [.4,.5,.6,.7,.8,.9,.95]:
  m=vc>=threshold; choices.append({'threshold':threshold,'val_accepted':int(m.sum()),'val_coverage':float(m.mean()),'val_accuracy':float((vy[m]==val.label.to_numpy()[m]).mean()) if m.any() else None})
 feasible=[x for x in choices if x['val_accuracy'] is not None and x['val_accuracy']>=.9 and x['val_accepted']>=100]
 threshold=max(feasible,key=lambda x:x['val_coverage'])['threshold'] if feasible else 1.0
 accepted=confidence>=threshold; truth=test.label.to_numpy(); wrong=int((accepted&(pred!=truth)).sum()); review=int((~accepted).sum())
 result={'status':'EXECUTED','sampling':'sha256(complaint_id) mod 100 < 3; exact normalized text deduplicated before split','sample_duplicate_texts_removed':duplicates,'train':len(train),'validation':len(val),'test':len(test),'taxonomy_window':'2018-05-01 to 2023-07-31; chronological split at 2022 and 2023','classes':list(model.classes_),'accuracy':accuracy_score(truth,pred),'macro_f1':f1_score(truth,pred,average='macro'),'majority_accuracy':float((truth==train.label.mode()[0]).mean()),'per_class':classification_report(truth,pred,output_dict=True,zero_division=0),'threshold_search':choices,'chosen_threshold':threshold,'test_accepted':int(accepted.sum()),'test_coverage':float(accepted.mean()),'test_selective_accuracy':float((pred[accepted]==truth[accepted]).mean()) if accepted.any() else None,'test_wrong_accepted':wrong,'test_human_review':review,'cost_scenarios':[{'wrong_route_cost_assumption':c,'review_cost_assumption':1,'total_units':c*wrong+review} for c in [5,10,25]],'llm_evaluation':'NOT EXECUTED; no authorised model endpoint configured','limitations':['Consumer-selected product is a proxy label, not institutional routing ground truth.','Chronological exact-text dedup does not remove all near-duplicate templates.','PII scrubbing is not a privacy guarantee; raw narratives excluded from publication.','Explicit product words may make classification easier; no causal or operational gain claim.']}
 t=time.perf_counter(); model.predict(T[:100]); result['warm_inference_ms_per_100']=(time.perf_counter()-t)*1000
 pd.DataFrame(confusion_matrix(truth,pred,labels=model.classes_),index=model.classes_,columns=model.classes_).to_csv(OUT/'cfpb_confusion.csv')
 (OUT/'cfpb_evaluation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if __name__=='__main__': main()
