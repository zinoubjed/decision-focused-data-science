"""Sensor alert reliability with explicit bin availability and event windows."""
import pandas as pd,numpy as np,zipfile
from sklearn.ensemble import IsolationForest
from common import ROOT,project,save,environment,configure_plot
P=project('PRJ5_metro')
EVENTS=[('2020-04-18 00:00','2020-04-18 23:59'),('2020-05-29 23:30','2020-05-30 06:00'),('2020-06-05 10:00','2020-06-07 14:30'),('2020-07-15 14:30','2020-07-15 19:00')]
def persistent(raw,k=3):return raw.astype(int).rolling(k,min_periods=k).sum().eq(k)
def episodes(alert):
 starts=alert&~alert.shift(fill_value=False);ends=alert&~alert.shift(-1,fill_value=False)
 return [(a,b) for a,b in zip(alert.index[starts],alert.index[ends])]
def evaluate(score,threshold,valid):
 alert=persistent(score.gt(threshold)&valid);eps=episodes(alert);windows=[];in_event=pd.Series(False,index=score.index)
 for a,b in EVENTS:
  a,b=pd.Timestamp(a),pd.Timestamp(b);mask=(score.index>=a)&(score.index<=b);in_event|=mask
  active=score.index[mask&alert];pre=score.index[(score.index>=a-pd.Timedelta(hours=24))&(score.index<a)&alert]
  windows.append({'start':str(a),'end':str(b),'valid_bins':int(valid[mask].sum()),'alert_during_event':bool(len(active)),'first_during_event':str(active[0]) if len(active) else None,'alert_prior_24h':bool(len(pre)),'earliest_prior_lead_minutes':float((a-pre[0]).total_seconds()/60) if len(pre) else None})
 outside=sum(not any(a<=pd.Timestamp(y) and b>=pd.Timestamp(x) for x,y in EVENTS) for a,b in eps)
 return {'threshold':float(threshold),'valid_bins':int(valid.sum()),'observed_days_equivalent':float(valid.sum()/144),'alert_bins':int(alert.sum()),'alert_hours':float(alert.sum()/6),'episodes':len(eps),'episodes_no_overlap_report':int(outside),'unverified_episodes_per_observed_day':float(outside/(valid.sum()/144)),'event_windows':windows},alert,eps
def main():
 # Reuse prepared sensor medians from the existing audit, no raw re-audit.
 d=pd.read_csv(ROOT/'reports/metro_10min.csv',index_col=0,parse_dates=True)
 with zipfile.ZipFile(ROOT/'data/raw/metro.zip') as z:
  timestamps=pd.to_datetime(pd.read_csv(z.open('MetroPT3(AirCompressor).csv'),usecols=['timestamp']).timestamp)
 coverage=pd.Series(1,index=timestamps).resample('10min').sum().reindex(d.index).fillna(0)
 d.loc[coverage<54,:]=np.nan # at least 90% of nominal 60 observations per bin
 d.index=d.index+pd.Timedelta(minutes=10) # aggregate becomes available at bin close
 train=d[d.index<='2020-03-01'];test=d[d.index>'2020-03-01'];tr=train.dropna();valid=test.notna().all(axis=1)
 median=tr.median();scale=(tr.quantile(.75)-tr.quantile(.25)).replace(0,1)
 train_z=(tr-median)/scale;test_z=(test-median)/scale
 simple_train=train_z.abs().max(axis=1);simple=test_z.abs().max(axis=1).where(valid)
 forest=IsolationForest(n_estimators=100,random_state=42,n_jobs=2).fit(train_z)
 ft=-forest.score_samples(train_z);fs=pd.Series(np.nan,index=test.index);fs.loc[valid]=-forest.score_samples(test_z[valid])
 rows=[];series=[];episode_rows=[]
 for model,ts,score in [('robust_max_deviation',simple_train.to_numpy(),simple),('isolation_forest',ft,fs)]:
  for q in [.99,.995,.999]:
   result,alert,eps=evaluate(score,float(np.quantile(ts,q)),valid);result.update(model=model,training_quantile=q);rows.append(result)
   if q==.995:
    series.append(pd.DataFrame({'time_available':test.index,'model':model,'score':score.to_numpy(),'valid':valid.to_numpy(),'alert':alert.to_numpy()}))
    episode_rows.extend({'model':model,'start':str(a),'end':str(b),'duration_bins':int((b-a).total_seconds()/600+1)} for a,b in eps)
 pd.concat(series).to_csv(P/'results/scores.csv',index=False);pd.DataFrame(episode_rows).to_csv(P/'results/episodes.csv',index=False)
 save(P/'results/metrics.json',{'training_valid_bins':len(tr),'test_bins':len(test),'test_invalid_bins':int((~valid).sum()),'bin_availability':'10-minute medians labeled by closing time; >=54 raw observations per bin and 3 consecutive valid bins for alert; missing/undercovered bins break persistence','results':rows,'event_source':'UCI official table; original intervals retained, duplicate ID/maintenance-date ambiguity unresolved','no_false_positive_ground_truth':True,'limits':['Only four report windows and one compressor.','Unverified outside-report episodes are not proven false positives.','Threshold grid is sensitivity analysis, not tuned on test event recall.','Sensor-range baseline uses robust IQR; zero IQR set to one.','No downtime reduction, safe shutdown or operational predictive-maintenance claim.'],'environment':environment()})
 plt=configure_plot();fig,axes=plt.subplots(2,1,figsize=(12,7),sharex=True)
 for ax,g in zip(axes,series):
  ax.plot(pd.to_datetime(g.time_available),g.score,lw=.5,label=g.model.iloc[0]);ax.legend();ax.set_ylabel('Anomaly score')
  for a,b in EVENTS:ax.axvspan(pd.Timestamp(a),pd.Timestamp(b),color='red',alpha=.2)
 axes[-1].set_xlabel('Bin closing time; red = reported event');fig.savefig(P/'figures/alerts.png');plt.close(fig)
 print('PRJ5',[(x['model'],x['training_quantile'],x['episodes']) for x in rows],flush=True)
if __name__=='__main__':main()
