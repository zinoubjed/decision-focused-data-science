"""Bounded, local-only zero-shot diagnostic; no sensitive text/output exported."""
import os,time
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1';os.environ['USE_TF']='0'
import pandas as pd,numpy as np,torch,joblib
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
from common import ROOT,WORK,project,save
P=project('PRJ4_cfpb')
def main():
 d=pd.read_parquet(ROOT/'data/processed/cfpb_model_splits.parquet');test=d[d.split=='test'];bundle=joblib.load(ROOT/'data/processed/cfpb_model.joblib');labels=list(bundle['model'].classes_)
 # Six chronological retained test cases per class, fixed before looking at predictions.
 subset=test.groupby('label',sort=True).head(6);assert len(subset)==54
 local=WORK/'flan-t5-small';tokenizer=AutoTokenizer.from_pretrained(local,local_files_only=True);model=AutoModelForSeq2SeqLM.from_pretrained(local,local_files_only=True);model.eval();torch.set_num_threads(2)
 options='\n'.join(f'{j+1}: {label}' for j,label in enumerate(labels));pred=[];latencies=[];invalid=0
 for text in subset.text:
  prompt=f'Classify this complaint into exactly one product category. Return only the category number. Categories:\n{options}\nComplaint: {text[:1200]}\nCategory number:'
  start=time.perf_counter();inputs=tokenizer(prompt,return_tensors='pt',max_length=512,truncation=True)
  with torch.no_grad():tokens=model.generate(**inputs,max_new_tokens=4,do_sample=False)
  output=tokenizer.decode(tokens[0],skip_special_tokens=True).strip();latencies.append(time.perf_counter()-start)
  if output in [str(j+1) for j in range(len(labels))]:pred.append(labels[int(output)-1])
  else:pred.append('ABSTAIN');invalid+=1
 base=bundle['model'].predict(bundle['vectorizer'].transform(subset.text));truth=subset.label.to_numpy()
 save(P/'results/local_llm_diagnostic.json',{'model':'google/flan-t5-small, pinned local revision in reports/model_manifest.json','evaluation':'54 retained chronological test cases, six per class; diagnostic only, class-balanced and not representative prevalence','n':len(subset),'llm_accuracy':float(accuracy_score(truth,pred)),'llm_macro_f1':float(f1_score(truth,pred,labels=labels,average='macro',zero_division=0)),'tfidf_accuracy_same_subset':float(accuracy_score(truth,base)),'tfidf_macro_f1_same_subset':float(f1_score(truth,base,labels=labels,average='macro')),'invalid_output_abstentions':invalid,'mean_seconds_including_tokenization':float(np.mean(latencies)),'p95_seconds':float(np.quantile(latencies,.95)),'prompt_limit':'first 1200 characters; max 512 input tokens; options included in limit','max_new_tokens':4,'external_model_api_calls':0,'api_charge':0,'cost_limit':'Local electricity/hardware cost not measured','privacy':'All inference local; no complaint text, prompt, generated text, vocabulary or ID exported. Only aggregate metrics/confusion labels.','decision':'No production selection from this small diagnostic; retain validated TF-IDF pipeline.','limits':['Tiny general model, no domain tuning.','Balanced 54-case sample differs from main temporal test.','Original taxonomy is a consumer-selected proxy.','Truncation may remove decisive evidence.']})
 pd.DataFrame(confusion_matrix(truth,pred,labels=labels+['ABSTAIN']),index=labels+['ABSTAIN'],columns=labels+['ABSTAIN']).to_csv(P/'results/local_llm_confusion.csv');print('CFPB local LLM diagnostic',len(subset),accuracy_score(truth,pred),flush=True)
if __name__=='__main__':main()
