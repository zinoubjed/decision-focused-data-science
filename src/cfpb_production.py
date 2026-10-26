"""Private local text processing; reports contain aggregates and labels only."""
import hashlib,re,zipfile,time,json
import pandas as pd,numpy as np,joblib
from sklearn.feature_extraction.text import TfidfVectorizer,HashingVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score,f1_score,classification_report,confusion_matrix
from common import ROOT,project,save,environment,wilson,configure_plot
P=project('PRJ4_cfpb');PRIVATE=ROOT/'data/processed';PRIVATE.mkdir(exist_ok=True)
def normalize(text):return ' '.join(str(text).lower().split())
def scrub(text):
 t=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',' EMAIL ',str(text));t=re.sub(r'\b\d{3}[-. ]\d{3}[-. ]\d{4}\b',' PHONE ',t);t=re.sub(r'\b\d{3,}\b',' NUMBER ',t);return t
def sample():
 p=PRIVATE/'cfpb_id_sample_v2.parquet';meta=PRIVATE/'cfpb_id_sample_v2_manifest.json'
 sources={}
 for record in json.loads((ROOT/'reports/cfpb_integrity.json').read_text()):
  archive=ROOT/'data/raw'/record['file']
  with archive.open('rb') as f:actual=hashlib.file_digest(f,'sha256').hexdigest()
  if actual!=record['sha256']:raise ValueError('CFPB archive fingerprint mismatch; cache cannot be trusted')
  sources[archive.name]=actual
 if p.exists() and meta.exists():
  provenance=json.loads(meta.read_text())
  with p.open('rb') as f:cache_hash=hashlib.file_digest(f,'sha256').hexdigest()
  if provenance.get('sources')==sources and provenance.get('cache_sha256')==cache_hash and provenance.get('sample_rule')=='sha256_first8_mod100_lt3_v1':return pd.read_parquet(p)
  raise ValueError('Private sample cache provenance mismatch; preserve and investigate before rebuilding')
 frames=[]
 for archive in sorted((ROOT/'data/raw').glob('CCDB*.zip')):
  with zipfile.ZipFile(archive) as z:
   for n in z.namelist():
    if not n.endswith('.csv'):continue
    for d in pd.read_csv(z.open(n),usecols=['Date received','Product','Consumer complaint narrative','Complaint ID'],dtype=str,chunksize=100000):
     d=d[d['Consumer complaint narrative'].notna()].copy()
     bucket=d['Complaint ID'].map(lambda x:int(hashlib.sha256(x.encode()).hexdigest()[:8],16)%100)
     frames.append(d[bucket<3])
  print('CFPB sampled',archive.name,flush=True)
 d=pd.concat(frames,ignore_index=True);d.columns=['date','label','text','id'];d['date']=pd.to_datetime(d.date);d.to_parquet(p,index=False)
 with p.open('rb') as f:cache_hash=hashlib.file_digest(f,'sha256').hexdigest()
 save(meta,{'sources':sources,'sample_rule':'sha256_first8_mod100_lt3_v1','cache_sha256':cache_hash,'rows':len(d)})
 return d
def near_duplicate_mask(train_text,query_text,threshold=.9):
 # Character hashing captures copy/edit templates without retaining a learned vocabulary.
 hv=HashingVectorizer(analyzer='char_wb',ngram_range=(3,5),n_features=2**16,alternate_sign=False,norm='l2')
 a=hv.transform(train_text);b=hv.transform(query_text);nn=NearestNeighbors(n_neighbors=1,metric='cosine',algorithm='brute',n_jobs=2).fit(a)
 sim=[]
 for j in range(0,b.shape[0],128):dist,_=nn.kneighbors(b[j:j+128]);sim.extend(1-dist[:,0])
 return np.asarray(sim)>=threshold,np.asarray(sim)
def main():
 raw=sample();d=raw[(raw.date>='2018-05-01')&(raw.date<'2023-08-01')].dropna().drop_duplicates('id').sort_values(['date','id']).copy()
 d['hash']=d.text.map(normalize).map(lambda x:hashlib.sha256(x.encode()).hexdigest());exact=int(d.hash.duplicated().sum());d=d.drop_duplicates('hash',keep='first');d['text']=d.text.map(scrub)
 train=d[d.date<'2022-01-01'].copy();val=d[(d.date>='2022-01-01')&(d.date<'2023-01-01')].copy();test=d[d.date>='2023-01-01'].copy()
 keep=train.label.value_counts();keep=keep[keep>=100].index
 excluded={n:int((~x.label.isin(keep)).sum()) for n,x in [('train',train),('validation',val),('test',test)]}
 train=train[train.label.isin(keep)];val=val[val.label.isin(keep)];test=test[test.label.isin(keep)]
 # Remove near matches to training from both evaluation splits; also val/test matches.
 vm,vs=near_duplicate_mask(train.text,val.text);tm,ts=near_duplicate_mask(train.text,test.text)
 cleaned_val=val[~vm];vtest,_=near_duplicate_mask(cleaned_val.text,test.text) if len(cleaned_val) else (np.zeros(len(test),dtype=bool),None)
 cleaned_test=test[~(tm|vtest)];cleaned_val=cleaned_val.copy();cleaned_test=cleaned_test.copy()
 assert train.date.max()<cleaned_val.date.min()<cleaned_test.date.min()
 assert not set(train.hash)&set(cleaned_val.hash);assert not set(train.hash)&set(cleaned_test.hash)
 train['split']='train';cleaned_val['split']='validation';cleaned_test['split']='test'
 pd.concat([train,cleaned_val,cleaned_test]).to_parquet(PRIVATE/'cfpb_model_splits.parquet',index=False)
 vec=TfidfVectorizer(min_df=3,max_features=30000,ngram_range=(1,2),sublinear_tf=True,strip_accents='unicode');X=vec.fit_transform(train.text);V=vec.transform(cleaned_val.text);T=vec.transform(cleaned_test.text)
 candidates={'logistic_tfidf':LogisticRegression(max_iter=600,C=1),'multinomial_nb':MultinomialNB(alpha=1)};validation={};timings={}
 for name,model in candidates.items():
  start=time.perf_counter();model.fit(X,train.label);timings[name]=time.perf_counter()-start;pred=model.predict(V);validation[name]=float(f1_score(cleaned_val.label,pred,average='macro'))
 chosen=max(validation,key=validation.get);model=candidates[chosen];pred=model.predict(T);prob=model.predict_proba(T);confidence=prob.max(axis=1);truth=cleaned_test.label.to_numpy()
 vp=model.predict_proba(V);vc=vp.max(axis=1);vy=model.classes_[vp.argmax(axis=1)];choices=[]
 for threshold in [.4,.5,.6,.7,.8,.9,.95]:
  mask=vc>=threshold;correct=int((vy[mask]==cleaned_val.label.to_numpy()[mask]).sum());n=int(mask.sum());lo,hi=wilson(correct,n)
  choices.append({'threshold':threshold,'accepted':n,'coverage':float(mask.mean()),'accuracy':correct/n if n else None,'accuracy_wilson_low':lo,'accuracy_wilson_high':hi})
 # Conservative: lower Wilson bound >=90%, not merely point estimate.
 feasible=[x for x in choices if x['accepted']>=100 and x['accuracy_wilson_low']>=.9];threshold=max(feasible,key=lambda x:x['coverage'])['threshold'] if feasible else 1.0
 accept=confidence>=threshold;wrong=int((accept&(pred!=truth)).sum());naccept=int(accept.sum());review=int((~accept).sum())
 start=time.perf_counter();model.predict(T[:min(100,len(truth))]);latency=time.perf_counter()-start
 results={'sample_rule':'SHA256(complaint_id) first 8 hex mod 100 <3, 3% ID sample; all 21 archives scanned','sample_narratives':len(raw),'taxonomy_window':'2018-05-01 through 2023-07-31; labels retained as published, no silent relabeling','exact_duplicates_removed_in_window':exact,'training':len(train),'validation_before_near_filter':len(val),'test_before_near_filter':len(test),'validation':len(cleaned_val),'test':len(cleaned_test),'near_duplicate_rule':'char_wb 3–5 gram hashing cosine >=0.90; validation/test vs training and test vs retained validation; not guaranteed semantic deduplication','near_validation_removed':int(vm.sum()),'near_test_removed':int((tm|vtest).sum()),'excluded_low_support_or_unseen_classes':excluded,'classes':list(model.classes_),'class_support_train':train.label.value_counts().to_dict(),'validation_macro_f1':validation,'selected_model':chosen,'fit_seconds':timings,'test_accuracy':float(accuracy_score(truth,pred)),'test_macro_f1':float(f1_score(truth,pred,average='macro')),'majority_accuracy':float((truth==train.label.mode()[0]).mean()),'test_per_class':classification_report(truth,pred,output_dict=True,zero_division=0),'threshold_selection':choices,'threshold':threshold,'accepted':naccept,'accepted_wrong':wrong,'human_review':review,'coverage':float(accept.mean()),'selective_accuracy':float((pred[accept]==truth[accept]).mean()) if naccept else None,'selective_accuracy_wilson':wilson(naccept-wrong,naccept),'cost_sensitivity':[{'wrong_suggestion_cost':c,'review_cost':1,'total_units':c*wrong+review,'all_review_units':len(truth)} for c in [5,10,25]],'warm_classifier_seconds_per_100_or_less':latency,'latency_excludes':'text vectorization, network, UI and human review','privacy':'Local-only text and vocabulary artifacts in ignored data/processed. No text, token vocabulary or complaint IDs exported in results. Regex scrubbing is incomplete.','environment':environment()}
 save(P/'results/metrics.json',results)
 joblib.dump({'vectorizer':vec,'model':model,'threshold':threshold},PRIVATE/'cfpb_model.joblib')
 cm=pd.DataFrame(confusion_matrix(truth,pred,labels=model.classes_),index=model.classes_,columns=model.classes_);cm.to_csv(P/'results/confusion.csv')
 plt=configure_plot();fig,ax=plt.subplots(figsize=(12,9));im=ax.imshow(cm.to_numpy(),cmap='Blues');ax.set_xticks(range(len(cm)),cm.columns,rotation=90,fontsize=7);ax.set_yticks(range(len(cm)),cm.index,fontsize=7);ax.set(xlabel='Suggested product',ylabel='Consumer-selected product',title='CFPB temporal test, after template filtering');fig.colorbar(im,ax=ax);fig.savefig(P/'figures/confusion.png');plt.close(fig)
 save(P/'results/error_summary.json',{'wrong_total':int((pred!=truth).sum()),'wrong_accepted':wrong,'review_volume':review,'no_text_examples_published':True,'largest_confusions':[{'actual':a,'predicted':b,'count':int(cm.loc[a,b])} for a,b in sorted([(a,b) for a in cm.index for b in cm.columns if a!=b],key=lambda ab:cm.loc[ab[0],ab[1]],reverse=True)[:10]]})
 print('PRJ4',chosen,results['test_macro_f1'],'review',review,flush=True)
if __name__=='__main__':main()
