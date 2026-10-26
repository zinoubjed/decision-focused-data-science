"""Auditable post-run rubric v2; no numeric-substring scoring or hardcoded totals."""
import json,re
from common import ROOT,save
P=ROOT/'projects/LAB1_rag'
EXTRA_ALIASES={
 'Is the library open on Sunday?':['no','the library is closed on sunday'],
 'Can digital book loans be renewed?':['no','digital loans cannot be renewed'],
 'How many renewals are allowed for a standard book?':['one','1'],
 'How many days does a standard book loan last?':['14 days'],
}
UNKNOWN={'unknown','not specified','not specified in this handbook','the handbook does not specify'}
def norm(text):return ' '.join(re.sub(r'[^a-z0-9:]+',' ',text.lower()).split())
def correct(question,expected,answerable,response):
 value=norm(response)
 if not answerable:return value in UNKNOWN
 return value in {norm(x) for x in [expected]+EXTRA_ALIASES.get(question,[])}
def main():
 source=json.loads((P/'results/evaluation_rows.json').read_text());rows=[];n_citations=0;n_relevant=0;n_correct=0
 for x in source:
  row={'question':x['question'],'answerable':x['answerable']}
  for key in ['baseline_answer','raw_rag_answer','guarded_answer']:row[key+'_correct']=correct(x['question'],x['expected'],x['answerable'],x[key])
  row['abstained']=norm(x['guarded_answer']) in UNKNOWN
  # Benchmark reference source is the original QA source where defined.
  # For known ambiguous short references use the explicitly declared QA document.
  source_by_question=['loans','loans','hours','hours','holds','holds','membership','returns','returns','rooms','rooms','rooms','digital','digital','digital','support','returns','support',None,None]
  if len(source)!=len(source_by_question):raise ValueError('Question set changed; reference-document rubric must be reviewed')
  i=len(rows);gold=source_by_question[i]+'.txt' if source_by_question[i] else None
  relevant=sum(c==gold for c in x['citations']);n_citations+=len(x['citations']);n_relevant+=relevant;n_correct+=relevant*int(row['guarded_answer_correct'])
  row['declared_reference_document']=gold;row['citation_count']=len(x['citations']);row['reference_document_matches']=relevant;rows.append(row)
 n=len(rows);accepted=[r for r in rows if not r['abstained']];unanswerable=[r for r in rows if not r['answerable']]
 result={'rubric':'v2 exact normalized accepted aliases, post-run scoring revision; not an untouched new benchmark','n':n,'baseline_correct':sum(r['baseline_answer_correct'] for r in rows),'raw_rag_correct':sum(r['raw_rag_answer_correct'] for r in rows),'guarded_correct':sum(r['guarded_answer_correct'] for r in rows),'baseline_accuracy':sum(r['baseline_answer_correct'] for r in rows)/n,'raw_rag_accuracy':sum(r['raw_rag_answer_correct'] for r in rows)/n,'guarded_accuracy':sum(r['guarded_answer_correct'] for r in rows)/n,'accepted':len(accepted),'accepted_correct':sum(r['guarded_answer_correct'] for r in accepted),'selective_accuracy':sum(r['guarded_answer_correct'] for r in accepted)/len(accepted) if accepted else None,'unanswerable':len(unanswerable),'correct_refusals':sum(r['abstained'] for r in unanswerable),'citation_count':n_citations,'reference_document_precision':n_relevant/n_citations if n_citations else None,'correct_answer_and_reference_fraction':n_correct/n_citations if n_citations else None,'limits':['Accepted aliases are an explicit restricted rubric, not a semantic entailment model.','Source-document agreement does not guarantee that the cited sentence supports the answer.','Original substring scores and generated outputs are preserved, not overwritten.','Rubric was clarified after inspecting outputs; no claim of blind human annotation.']}
 save(P/'results/scoring_v2.json',result);save(P/'results/scored_rows_v2.json',rows);save(P/'results/rubric_v2.json',{'extra_aliases':EXTRA_ALIASES,'unknown_aliases':sorted(UNKNOWN),'criterion':'exact normalized match, not substring','source_by_question':source_by_question});print('RAG rubric v2:',result,flush=True)
if __name__=='__main__':main()
