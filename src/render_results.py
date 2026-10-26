"""Presentation-only regeneration from measured tables; no refitting."""
import pandas as pd,numpy as np,json
from common import ROOT,configure_plot,save
def main():
 plt=configure_plot();retail=ROOT/'projects/PRJ2_retail';rm=json.loads((retail/'results/metrics.json').read_text());primary=None
 for name,metric in rm['variants'].items():
  d=pd.read_csv(retail/'results'/f'backtest_{name}.csv');chosen=metric['selected_on_validation'];g=d[(d.model==chosen)&(d.t>=d.t.max()-25)].copy();mask=g.target_end.isin(metric['interval']['evaluation_target_dates']);q=metric['interval']['calibration_absolute_error_GBP'];g['interval_phase']=np.where(mask,'evaluation','calibration');g['lower']=np.where(mask,np.maximum(0,g.forecast-q),np.nan);g['upper']=np.where(mask,g.forecast+q,np.nan);assessed=g[mask]
  assert np.isclose(((assessed.actual>=assessed.lower)&(assessed.actual<=assessed.upper)).mean(),metric['interval']['test_coverage'])
  g.to_csv(retail/'results'/f'predictions_with_intervals_{name}.csv',index=False)
  if name==rm['primary']:primary=g
 fig,ax=plt.subplots();x=pd.to_datetime(primary.target_end);mask=primary.interval_phase.eq('evaluation');ax.plot(x,primary.actual,label='Observed positive sales');ax.plot(x,primary.forecast,label='Validation-selected seasonal naive');ax.fill_between(x,primary.lower,primary.upper,alpha=.2,label='Scenario, final 13 weeks only');ax.axvline(x[mask].iloc[0],ls='--',color='gray',label='Interval evaluation begins');ax.set(ylabel='GBP per week',title='26 point forecasts; nominal-90% scenario covers 8/13 final weeks');ax.legend(fontsize=9);fig.autofmt_xdate();fig.savefig(retail/'figures/backtest.png');plt.close(fig)
 p=ROOT/'projects/PRJ4_cfpb';c=pd.read_csv(p/'results/confusion.csv',index_col=0);a=c.div(c.sum(axis=1),axis=0)
 aliases=['Checking / savings','Credit / prepaid card','Credit reporting','Debt collection','Money services','Mortgage','Payday / personal loan','Student loan','Vehicle finance'];fig,ax=plt.subplots(figsize=(10,8));im=ax.imshow(a,vmin=0,vmax=1,cmap='Blues')
 ax.set_xticks(range(9),aliases,rotation=35,ha='right');ax.set_yticks(range(9),[f'{x} (n={int(n)})' for x,n in zip(aliases,c.sum(axis=1))]);ax.set(xlabel='Suggested category',ylabel='Consumer-selected category',title='CFPB: temporal test confusions, normalized by actual class')
 for i in range(9):
  for j in range(9):
   if a.iloc[i,j]>=.04:ax.text(j,i,f'{a.iloc[i,j]:.0%}',ha='center',va='center',fontsize=9,color='white' if a.iloc[i,j]>.5 else 'black')
 fig.colorbar(im,ax=ax,label='Fraction of actual class');fig.savefig(p/'figures/confusion.png');plt.close(fig)
 from score_rag import main as score_outputs
 score_outputs();p=ROOT/'projects/LAB1_rag';rubric=json.loads((p/'results/scoring_v2.json').read_text())
 fig,ax=plt.subplots();ax.bar(['No RAG','Raw RAG','Guarded RAG'],[rubric['baseline_accuracy'],rubric['raw_rag_accuracy'],rubric['guarded_accuracy']],color=['#9baeb7','#25837c','#173d51']);ax.set(ylim=(0,1),ylabel='Answer correctness under explicit alias rubric',title=f"Local FLAN-T5-small: rubric v2, n={rubric['n']}");ax.text(.02,.97,'Post-run rubric clarification; not independent human evaluation',transform=ax.transAxes,va='top',fontsize=9);fig.savefig(p/'figures/comparison.png');plt.close(fig)
 print('presentation figures reviewed and regenerated',flush=True)
if __name__=='__main__':main()
