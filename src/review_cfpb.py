"""Expanded, local-only evaluation of the already-fitted classifier and review burden."""
import hashlib,json
import numpy as np,pandas as pd,joblib
from common import ROOT,project,save,wilson
from cfpb_production import sample,normalize
P=project('PRJ4_cfpb')
def main():
 raw=sample();old=ROOT/'data/processed/cfpb_id_sample.parquet'
 old_equal=bool(raw.equals(pd.read_parquet(old))) if old.exists() else None
 if old_equal is False:raise ValueError('Fresh sample differs from original fitted-data sample; refit/review required')
 private=pd.read_parquet(ROOT/'data/processed/cfpb_model_splits.parquet');test=private[private.split=='test'].copy();bundle=joblib.load(ROOT/'data/processed/cfpb_model.joblib');model=bundle['model'];T=bundle['vectorizer'].transform(test.text);proba=model.predict_proba(T);pred=model.classes_[proba.argmax(axis=1)];accept=proba.max(axis=1)>=bundle['threshold'];truth=test.label.to_numpy()
 rows=[]
 for label in model.classes_:
  mask=truth==label;n=int(mask.sum());accepted=int((mask&accept).sum());correct=int((mask&accept&(pred==truth)).sum())
  rows.append({'actual_class':label,'test_support':n,'accepted':accepted,'accepted_correct':correct,'accepted_wrong':accepted-correct,'review':n-accepted,'coverage':accepted/n if n else None,'accepted_accuracy':correct/accepted if accepted else None,'accepted_accuracy_wilson':wilson(correct,accepted)})
 save(P/'results/selective_by_actual_class.json',rows)
 window=raw[(raw.date>='2018-05-01')&(raw.date<'2023-08-01')].dropna().drop_duplicates('id').sort_values(['date','id']).copy()
 before=window[window.date>='2023-01-01'];n_all=len(before)
 window['hash']=window.text.map(normalize).map(lambda x:hashlib.sha256(x.encode()).hexdigest());after=window.drop_duplicates('hash',keep='first');after_test=after[after.date>='2023-01-01'];excluded_classes=int((~after_test.label.isin(model.classes_)).sum());n_accept=int(accept.sum());wrong=int((accept&(pred!=truth)).sum());near=len(after_test)-excluded_classes-len(test)
 save(P/'results/decision_population.json',{'population':'3% ID-sampled 2023-01-01 to 2023-07-31 narratives in fixed taxonomy window, after required-field/ID checks','sampled_test_before_text_filter':n_all,'exact_repeat_review':n_all-len(after_test),'unsupported_class_review':excluded_classes,'near_repeat_review':near,'retained_novel_test':len(test),'novel_low_confidence_review':int((~accept).sum()),'accepted_suggestions':n_accept,'accepted_wrong':wrong,'total_manual_review_if_duplicate_gate_is_deployed':n_all-n_accept,'acceptance_fraction_over_all_sampled_test':n_accept/n_all,'review_fraction_over_all_sampled_test':1-n_accept/n_all,'cost_scenarios_including_withheld_cases':[{'wrong_cost_assumption':c,'review_cost_assumption':1,'total_units':wrong*c+n_all-n_accept,'review_all_units':n_all} for c in [5,10,25]],'interpretation':'Duplicate/unsupported cases are assigned to review, not silently removed from workload. This is a hypothetical gate on a sample, not measured institution productivity.','fresh_sample_identical_to_original':old_equal,'limitations':['No calibrated probability guarantee.','Wilson bounds used during threshold search are descriptive, not post-selection guarantees.','Rare-class accepted volumes can be too small for reliable quality claims.']})
 assert n_all-n_accept==(n_all-len(after_test))+excluded_classes+near+int((~accept).sum())
 print('CFPB overall sampled workflow:',n_all,'accepted',n_accept,'review',n_all-n_accept,'fresh sample matched:',old_equal,flush=True)
if __name__=='__main__':main()
