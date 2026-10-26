"""LAB1: real local FLAN-T5 generation on authored fictional policy documents."""
import os,time,re,hashlib
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1';os.environ['USE_TF']='0'
import numpy as np,pandas as pd,torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
from common import ROOT,WORK,project,save,environment,configure_plot
P=project('LAB1_rag');CORPUS=P/'corpus';CORPUS.mkdir(exist_ok=True)
DOCS={
 'loans':'Lumen Library is a fictional benchmark organisation. Standard book loans last 14 days. A member may renew a book once, provided no other member has reserved it. Reference books must remain inside the library.',
 'hours':'Lumen Library opens at 09:00 from Monday to Friday and closes at 18:00. Saturday opening is 10:00 to 14:00. The library is closed on Sunday. These are fictional benchmark rules, not real opening hours.',
 'holds':'Lumen Library reservations are held for 3 days after notification. Members can reserve at most 4 books at once. Uncollected reservations are released to the next member after the holding period.',
 'membership':'Lumen Library membership is free. A member must present an identification document at registration. The fictional benchmark stores no identity documents or personal information. Guest access allows reading on site only.',
 'returns':'Lumen Library accepts book returns at the main desk during opening hours. There is no outdoor return box. A damaged book must be reported to a librarian. The replacement fee for damaged books is not specified in this handbook.',
 'rooms':'Lumen Library study rooms can be booked for 2 hours. A group can have at most 6 people. A booking is cancelled if nobody arrives within 15 minutes. Food is prohibited in study rooms.',
 'digital':'Lumen Library digital books expire after 21 days. Digital loans cannot be renewed. Members can borrow at most 5 digital books at a time. Offline access requires downloading before the loan expires.',
 'support':'Lumen Library support replies within 2 working days. Questions about lost property are handled by the main desk. The handbook does not specify a phone number or an email address. Never invent contact details.'}
QA=[('How many days does a standard book loan last?','14','loans',True),('How many renewals are allowed for a standard book?','once','loans',True),('When does the library open on weekdays?','09:00','hours',True),('Is the library open on Sunday?','closed','hours',True),('How long are reservations held after notification?','3 days','holds',True),('What is the maximum number of simultaneous reservations?','4','holds',True),('What is the membership price?','free','membership',True),('Where should books be returned?','main desk','returns',True),('Is there an outdoor return box?','no','returns',True),('How long can a study room be booked?','2 hours','rooms',True),('How many people can use a study room together?','6','rooms',True),('After how many minutes of absence is a room booking cancelled?','15','rooms',True),('How long does a digital book loan last?','21 days','digital',True),('Can digital book loans be renewed?','cannot','digital',True),('How many digital books can a member borrow?','5','digital',True),('What is the support response time?','2 working days','support',True),('What is the replacement fee for a damaged book?','UNKNOWN','returns',False),('What is the library phone number?','UNKNOWN','support',False),('Who is the current library director?','UNKNOWN',None,False),('What is the price of a library parking ticket?','UNKNOWN',None,False)]
def norm(x):return re.sub(r'[^a-z0-9:]+',' ',x.lower()).strip()
def main():
 for name,text in DOCS.items():(CORPUS/f'{name}.txt').write_text(text,encoding='utf-8')
 chunks=[]
 for p in sorted(CORPUS.glob('*.txt')):
  # Each short policy document is one <=100-word chunk. No arbitrary sentence overlap.
  chunks.append({'id':p.stem,'text':p.read_text(),'source':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 vec=TfidfVectorizer(ngram_range=(1,2),stop_words='english');X=vec.fit_transform([x['text'] for x in chunks]);svd=TruncatedSVD(n_components=7,random_state=42);emb=normalize(svd.fit_transform(X))
 # Dense latent-semantic embeddings suit this tiny lexical policy corpus; no neural-embedding claim.
 torch.set_num_threads(2);torch.manual_seed(42);model_dir=WORK/'flan-t5-small'
 tokenizer=AutoTokenizer.from_pretrained(model_dir,local_files_only=True);model=AutoModelForSeq2SeqLM.from_pretrained(model_dir,local_files_only=True);model.eval()
 def generate(prompt):
  t=time.perf_counter();inputs=tokenizer(prompt,return_tensors='pt',truncation=True,max_length=512)
  with torch.no_grad():tokens=model.generate(**inputs,max_new_tokens=48,do_sample=False)
  return tokenizer.decode(tokens[0],skip_special_tokens=True),time.perf_counter()-t
 rows=[]
 for question,expected,source,answerable in QA:
  q=normalize(svd.transform(vec.transform([question])));sim=(q@emb.T)[0];ids=np.argsort(sim)[-2:][::-1];context='\n'.join(f'[{chunks[i]["id"]}] {chunks[i]["text"]}' for i in ids)
  raw,seconds=generate(f'Answer the question using only the context. If the answer is not in the context, answer UNKNOWN. Give a short answer.\nContext: {context}\nQuestion: {question}\nAnswer:')
  base,bseconds=generate(f'Answer briefly. If you do not know, answer UNKNOWN. Question: {question}\nAnswer:')
  # Mechanical guard uses only source support, never expected answers.
  unsupported=norm(raw) not in norm(context);unknown='unknown' in norm(raw) or norm(raw) in ['not specified','not specified in this handbook'];guarded='UNKNOWN' if unknown or unsupported or float(sim[ids[0]])<.15 else raw
  correct=(norm(expected) in norm(raw)) if answerable else unknown
  guarded_correct=(norm(expected) in norm(guarded)) if answerable else guarded=='UNKNOWN'
  baseline_correct=(norm(expected) in norm(base)) if answerable else 'unknown' in norm(base)
  rows.append({'question':question,'expected':expected,'answerable':answerable,'retrieved':[chunks[i]['id'] for i in ids],'retrieval_hit':source in [chunks[i]['id'] for i in ids] if source else None,'raw_rag_answer':raw,'guarded_answer':guarded,'citations':[] if guarded=='UNKNOWN' else [chunks[i]['source'] for i in ids if norm(raw) in norm(chunks[i]['text'])],'baseline_answer':base,'raw_correct':bool(correct),'guarded_correct':bool(guarded_correct),'baseline_correct':bool(baseline_correct),'raw_unsupported_by_substring':bool(unsupported and not unknown),'guard_abstained':guarded=='UNKNOWN','rag_generation_seconds':seconds,'baseline_generation_seconds':bseconds,'retrieval_similarity':float(sim[ids[0]])})
 d=pd.DataFrame(rows);save(P/'results/evaluation_rows.json',rows);save(P/'results/corpus_manifest.json',chunks)
 # Heuristic metrics are explicitly not a human semantic faithfulness review.
 save(P/'results/metrics.json',{'questions':len(rows),'answerable':sum(x[3] for x in QA),'raw_exact_reference_accuracy':float(d.raw_correct.mean()),'guarded_exact_reference_accuracy':float(d.guarded_correct.mean()),'no_rag_exact_reference_accuracy':float(d.baseline_correct.mean()),'retrieval_hit_at_2':float(d.retrieval_hit.dropna().astype(float).mean()),'raw_unsupported_substring_fraction':float(d.raw_unsupported_by_substring.mean()),'guard_abstention_fraction':float(d.guard_abstained.mean()),'correct_unknown_on_unanswerable':int(((~d.answerable)&d.guard_abstained).sum()),'rag_mean_generation_seconds':float(d.rag_generation_seconds.mean()),'no_rag_mean_generation_seconds':float(d.baseline_generation_seconds.mean()),'embeddings':'7-dimensional truncated-SVD latent semantic embeddings on TF-IDF, fit corpus only','model':'google/flan-t5-small; Apache-2.0, revision/checksums in model_manifest.json','compute':'CPU local, 2 torch threads, deterministic greedy decoding','external_api_calls':0,'api_usage_cost':0,'cost_limit':'Electricity and hardware cost not measured; zero API charge does not mean zero total cost.','limits':['20 authored questions, used as a fixed diagnostic set, not broad generalization.','Expected-answer substring accuracy and source-substring support are mechanical proxies; negation and aliases need human semantic review.','Guard may reject valid paraphrases and may accept a supported phrase answering the wrong question.','Toy fictional policies, no personal data, no actual institutional rules.'],'environment':environment()})
 plt=configure_plot();fig,ax=plt.subplots();ax.bar(['No RAG','Raw RAG','Guarded RAG'],[d.baseline_correct.mean(),d.raw_correct.mean(),d.guarded_correct.mean()],color=['#9baeb7','#25837c','#173d51']);ax.set(ylim=(0,1),ylabel='Reference substring accuracy',title='Local FLAN-T5-small: fixed 20-question diagnostic');fig.savefig(P/'figures/comparison.png');plt.close(fig);print('LAB1 measured',d.guarded_correct.mean(),flush=True)
 from score_rag import main as score_outputs
 score_outputs()
if __name__=='__main__':main()
