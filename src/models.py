"""Measured chronological baselines; costs are sensitivity assumptions only."""
import pathlib,json,pandas as pd,numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import Ridge
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'reports'
def save(n,x): (OUT/f'{n}.json').write_text(json.dumps(x,indent=2,default=str),encoding='utf-8')
def retail():
 s=pd.read_csv(OUT/'retail_weekly.csv',index_col=0).iloc[:,0]; y=s.to_numpy(); rows=[]; intervals=[]
 # Calibration uses earlier errors only. Fixed 1-week horizon; last 26 origins held out.
 for t in range(53,len(y)):
  pred={'last_week':y[t-1],'annual_seasonal':y[t-52],'recent_4_mean':y[t-4:t].mean()}
  for name,p in pred.items(): rows.append({'origin':s.index[t-1],'target':s.index[t],'model':name,'actual':y[t],'forecast':p,'error':y[t]-p})
 d=pd.DataFrame(rows); test_dates=s.index[-26:]; test=d[d.target.isin(test_dates)]; cal=d[~d.target.isin(test_dates)]
 selection=cal.groupby('model').error.apply(lambda x:float(x.abs().mean())).sort_values(); chosen=selection.index[0]
 results={}
 for name,g in test.groupby('model'):
  errors=g.error.to_numpy(); results[name]={'n_weeks':len(g),'MAE_GBP':float(np.abs(errors).mean()),'WAPE':float(np.abs(errors).sum()/g.actual.abs().sum()),'bias_GBP':float(errors.mean())}
 cg=cal[cal.model==chosen]; q=float(np.quantile(np.abs(cg.error),.9,method='higher')); g=test[test.model==chosen].copy(); g['lower']=np.maximum(0,g.forecast-q); g['upper']=g.forecast+q
 results['selection']={'method':'minimum MAE on origins before final 26 weeks','selected':chosen,'calibration_weeks':len(cg),'absolute_error_90_quantile_GBP':q,'test_coverage':float(((g.actual>=g.lower)&(g.actual<=g.upper)).mean()),'caveat':'Small calibration set, serial dependence, no guaranteed coverage.'}
 g.to_csv(OUT/'retail_predictions.csv',index=False); save('retail_evaluation',results)
def metro():
 d=pd.read_csv(OUT/'metro_10min.csv',index_col=0,parse_dates=True)
 train=d[d.index<'2020-03-01']; test=d[d.index>='2020-03-01']; valid=train.dropna()
 median=valid.median(); scale=(valid.quantile(.75)-valid.quantile(.25)).replace(0,1)
 model=IsolationForest(n_estimators=100,random_state=42,n_jobs=2).fit((valid-median)/scale)
 cal=-model.score_samples((valid-median)/scale); score=pd.Series(np.nan,index=test.index); ok=test.notna().all(axis=1); score.loc[ok]=-model.score_samples((test.loc[ok]-median)/scale)
 events=[('2020-04-18 00:00','2020-04-18 23:59'),('2020-05-29 23:30','2020-05-30 06:00'),('2020-06-05 10:00','2020-06-07 14:30'),('2020-07-15 14:30','2020-07-15 19:00')]
 results=[]
 for q in [.99,.995,.999]:
  threshold=float(np.quantile(cal,q)); raw=score.gt(threshold); alert=raw.rolling(3,min_periods=3).sum().eq(3); starts=alert & ~alert.shift(fill_value=False); event_mask=pd.Series(False,index=test.index); hits=[]
  for a,b in events:
   a=pd.Timestamp(a); b=pd.Timestamp(b); mask=(test.index>=a)&(test.index<=b); event_mask|=mask
   hits.append({'start':str(a),'end':str(b),'alert_in_event':bool(alert[mask].any()),'alert_in_prior_24h':bool(alert[(test.index>=a-pd.Timedelta('24h'))&(test.index<a)].any())})
  results.append({'train_score_quantile':q,'threshold':threshold,'valid_test_bins':int(ok.sum()),'alert_bins':int(alert.sum()),'alert_episodes':int(starts.sum()),'outside_report_episodes':int((starts&~event_mask).sum()),'outside_report_episodes_per_observed_day':float((starts&~event_mask).sum()/(ok.sum()/144)),'events':hits})
 save('metro_evaluation',{'train_rows_10min':len(valid),'test_rows_10min':len(test),'test_missing_bins':int((~ok).sum()),'model':'IsolationForest, first calendar month only, 10-minute medians','persistence':'3 consecutive bins; one episode per contiguous alert','results':results,'warning':'Outside-report alerts are unverified alerts, not proven false positives. Four events cannot establish generalisation. Report has duplicated event ID and inconsistent maintenance date; original intervals preserved.'})
if __name__=='__main__':
 if (OUT/'retail_weekly.csv').exists(): retail()
 if (OUT/'metro_10min.csv').exists(): metro()
