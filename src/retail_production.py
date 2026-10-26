"""Positive observed sales, weekly 1-step backtesting with cleaning sensitivity."""
import zipfile,sqlite3,math
from datetime import timedelta
import pandas as pd,numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from common import ROOT,project,save,metrics,environment,configure_plot
P=project('PRJ2_retail')
LAGS=[1,2,4,13,52]
def features(y,t):
 return [np.log1p(y[t-k]) for k in LAGS]+[np.sin(2*np.pi*t/52),np.cos(2*np.pi*t/52)]
def evaluate(s):
 y=s.to_numpy();rows=[]
 for t in range(65,len(y)):
  preds={'last_week':y[t-1],'seasonal_52':y[t-52],'mean_4':y[t-4:t].mean()}
  ix=range(52,t);X=np.array([features(y,j) for j in ix]);target=np.log1p(y[52:t])
  reg=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit(X,target)
  preds['ridge_log_lags']=max(0,float(np.expm1(reg.predict([features(y,t)])[0])))
  for name,p in preds.items():rows.append({'origin_end':str(s.index[t-1]),'decision_time':str(s.index[t-1].to_pydatetime()+timedelta(days=1)),'target_end':str(s.index[t]),'t':t,'model':name,'actual':float(y[t]),'forecast':float(p)})
 d=pd.DataFrame(rows);cut=len(y)-26; val=d[d.t<cut];test=d[d.t>=cut]
 choice=val.assign(ae=(val.actual-val.forecast).abs()).groupby('model').ae.mean().idxmin()
 result={name:metrics(g.actual.to_numpy(),g.forecast.to_numpy()) for name,g in test.groupby('model')}
 g=test[test.model==choice].copy();cal=g.iloc[:13];evaluation=g.iloc[13:]
 errors=(cal.actual-cal.forecast).abs().to_numpy();rank=min(len(errors),math.ceil((len(errors)+1)*.9));q=float(np.sort(errors)[rank-1])
 g['interval_phase']=['calibration']*13+['evaluation']*len(evaluation)
 g['lower']=np.where(g.interval_phase.eq('evaluation'),np.maximum(0,g.forecast-q),np.nan);g['upper']=np.where(g.interval_phase.eq('evaluation'),g.forecast+q,np.nan)
 assessed=g[g.interval_phase.eq('evaluation')]
 result.update(selected_on_validation=choice,validation_origins=int(val.t.nunique()),test_origins=int(test.t.nunique()),interval={'nominal':.9,'calibration_absolute_error_GBP':q,'calibration_weeks':13,'evaluation_weeks':len(assessed),'calibration_target_dates':cal.target_end.tolist(),'evaluation_target_dates':assessed.target_end.tolist(),'test_coverage':float(((assessed.actual>=assessed.lower)&(assessed.actual<=assessed.upper)).mean()),'mean_width_GBP':float((assessed.upper-assessed.lower).mean()),'guarantee':'none: temporal dependence; separate chronological selection/calibration/evaluation blocks'},cost_scenarios=[{'underforecast_relative_cost':c,'overforecast_relative_cost':1,'total_assumed_cost_units':float((c*np.maximum(g.actual-g.forecast,0)+np.maximum(g.forecast-g.actual,0)).sum())} for c in [1,2,5]])
 return d,g,result
def main():
 with zipfile.ZipFile(ROOT/'data/raw/retail.zip') as z:
  book=next(n for n in z.namelist() if n.endswith('.xlsx'));df=pd.concat(pd.read_excel(z.open(book),sheet_name=None).values(),ignore_index=True)
 df.columns=['invoice','stock','description','quantity','date','price','customer','country'];df['date']=pd.to_datetime(df.date)
 cancelled=df.invoice.astype(str).str.upper().str.startswith('C');positive=df[~cancelled&df.quantity.gt(0)&df.price.gt(0)].copy();positive['revenue']=positive.quantity*positive.price
 diagnostics={'cancelled_lines':int(cancelled.sum()),'negative_quantity_lines':int(df.quantity.lt(0).sum()),'negative_quantity_signed_value_GBP':float((df.loc[df.quantity.lt(0),'quantity']*df.loc[df.quantity.lt(0),'price']).sum()),'positive_before_dedup_rows':len(positive),'positive_duplicate_rows':int(positive.duplicated().sum()),'target':'positive recorded sales value, GBP; not net revenue or latent demand'}
 variants={};predictions={}
 for name,data in [('retain_ambiguous_duplicates',positive),('remove_exact_duplicates',positive.drop_duplicates())]:
  s=data.set_index('date').revenue.resample('W-SUN').sum().iloc[1:-1];s.to_csv(P/'results'/f'weekly_{name}.csv')
  d,g,r=evaluate(s);variants[name]=r;predictions[name]=g;d.to_csv(P/'results'/f'backtest_{name}.csv',index=False);g.to_csv(P/'results'/f'predictions_with_intervals_{name}.csv',index=False)
 # Primary retains ambiguous lines: no evidence exact repeats are erroneous.
 primary='retain_ambiguous_duplicates';sel=variants[primary]['selected_on_validation'];s=positive.set_index('date').revenue.resample('W-SUN').sum().iloc[1:-1];y=s.to_numpy();t=len(y)
 if sel=='seasonal_52':next_pred=y[-52]
 elif sel=='last_week':next_pred=y[-1]
 elif sel=='mean_4':next_pred=y[-4:].mean()
 else:
  reg=make_pipeline(StandardScaler(),Ridge(alpha=10)).fit([features(y,j) for j in range(52,t)],np.log1p(y[52:t]));next_pred=float(np.expm1(reg.predict([features(y,t)])[0]))
 q=variants[primary]['interval']['calibration_absolute_error_GBP'];scenario={'origin_completed_week':str(s.index[-1]),'decision_time':str(s.index[-1].to_pydatetime()+timedelta(days=1)),'next_week_end':str(s.index[-1].to_pydatetime()+timedelta(days=7)),'central_GBP':float(next_pred),'low_GBP':max(0,float(next_pred-q)),'high_GBP':float(next_pred+q),'decision':'human workload/revenue scenario review only; no stock/capacity purchase authorised','historical_replay':True}
 save(P/'results/metrics.json',{'diagnostics':diagnostics,'primary':primary,'variants':variants,'planning_scenario':scenario,'environment':environment()})
 plt=configure_plot();g=predictions[primary];x=pd.to_datetime(g.target_end)
 fig,ax=plt.subplots();ax.plot(x,g.actual,label='Observed positive sales');ax.plot(x,g.forecast,label=sel);ax.fill_between(x,g.lower,g.upper,alpha=.2,label='Historical error scenario');ax.set(ylabel='GBP per week',title='Retail: final 26 one-week forecasts');ax.legend();fig.autofmt_xdate();fig.savefig(P/'figures/backtest.png');plt.close(fig)
 errors=g.assign(month=pd.to_datetime(g.target_end).dt.strftime('%Y-%m'),absolute_error=(g.actual-g.forecast).abs(),signed_error=g.actual-g.forecast).groupby('month').agg(weeks=('actual','size'),MAE_GBP=('absolute_error','mean'),bias_GBP=('signed_error','mean'));errors.to_csv(P/'results/error_by_month.csv')
 sql="""WITH RECURSIVE totals AS (
 SELECT date(date, '+' || ((7-CAST(strftime('%w',date) AS INTEGER))%7) || ' days') AS week_end,
 SUM(quantity*price) AS positive_sales FROM lines
 WHERE quantity>0 AND price>0 AND upper(substr(invoice,1,1))<>'C' GROUP BY week_end
 ), calendar(week_end) AS (
 SELECT MIN(week_end) FROM totals UNION ALL
 SELECT date(week_end,'+7 days') FROM calendar WHERE week_end<(SELECT MAX(week_end) FROM totals)
 ) SELECT c.week_end,COALESCE(t.positive_sales,0) AS positive_sales
 FROM calendar c LEFT JOIN totals t USING(week_end) ORDER BY c.week_end"""
 (P/'aggregation.sql').write_text('-- Sunday-ending calendar labels, matching pandas W-SUN.\n'+sql)
 db=sqlite3.connect(':memory:');df[['invoice','quantity','price','date']].to_sql('lines',db,index=False);sql_weeks=pd.read_sql_query(sql,db);sql_weeks['week_end']=pd.to_datetime(sql_weeks.week_end);pd_weeks=positive.set_index('date').revenue.resample('W-SUN').sum();assert np.array_equal(sql_weeks.week_end.to_numpy(),pd_weeks.index.to_numpy());assert np.allclose(sql_weeks.positive_sales,pd_weeks,rtol=1e-12,atol=1e-6)
 sql_total=sql_weeks.positive_sales.sum();save(P/'results/sql_check.json',{'sql_total_GBP':float(sql_total),'pandas_total_GBP':float(positive.revenue.sum()),'weekly_labels_and_values_match':True,'weeks_reconciled':len(sql_weeks),'passed':True})
 print('PRJ2',sel,variants[primary][sel],flush=True)
if __name__=='__main__':main()
