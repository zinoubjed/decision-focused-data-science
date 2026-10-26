"""Noncommercial retrospective delivery investigation; order-grain SQL."""
import sqlite3,html
import pandas as pd,numpy as np
from common import ROOT,project,save,table,wilson,environment,configure_plot
P=project('PRJ3_olist')
SQL='''WITH item_summary AS (
 SELECT order_id,COUNT(*) AS item_count,COUNT(DISTINCT seller_id) AS sellers,
 SUM(price) AS item_value,SUM(freight_value) AS freight_value FROM items GROUP BY order_id
), payment_summary AS (
 SELECT order_id,COUNT(*) AS payment_rows,SUM(payment_value) AS paid FROM payments GROUP BY order_id
), review_summary AS (
 SELECT order_id,COUNT(*) AS review_rows,AVG(review_score) AS mean_review_score FROM reviews GROUP BY order_id
)
SELECT o.*, c.customer_state,i.item_count,i.sellers,i.item_value,i.freight_value,p.payment_rows,p.paid,r.review_rows,r.mean_review_score
FROM orders o LEFT JOIN customers c USING(customer_id)
LEFT JOIN item_summary i USING(order_id) LEFT JOIN payment_summary p USING(order_id)
LEFT JOIN review_summary r USING(order_id)'''
def segment(d,col):
 g=d.groupby(col).agg(delivered=('order_id','size'),late=('late','sum'));g['late_rate']=g.late/g.delivered
 ci=[wilson(k,n) for k,n in zip(g.late,g.delivered)];g['wilson_low']=[x[0] for x in ci];g['wilson_high']=[x[1] for x in ci];g['review_eligible']=g.delivered.ge(100)
 return g
def main():
 db=sqlite3.connect(':memory:')
 for t in ['orders','customers','order_items','order_payments','order_reviews']:
  name={'order_items':'items','order_payments':'payments','order_reviews':'reviews'}.get(t,t)
  table('olist.zip',f'olist_{t}_dataset.csv').to_sql(name,db,index=False)
 d=pd.read_sql_query(SQL,db);assert d.order_id.is_unique and len(d)==99441
 (P/'order_grain.sql').write_text(SQL,encoding='utf-8')
 for c in [x for x in d if x.endswith('_date') or x.endswith('_at') or x.endswith('_timestamp')]:d[c]=pd.to_datetime(d[c],errors='coerce')
 d['cohort']=d.order_purchase_timestamp.dt.to_period('M').astype(str)
 d['outcome_available']=d.order_status.eq('delivered')&d.order_delivered_customer_date.notna()&d.order_estimated_delivery_date.notna()
 d['late']=(d.order_delivered_customer_date.dt.normalize()>d.order_estimated_delivery_date.dt.normalize())&d.outcome_available
 d['late_days']=(d.order_delivered_customer_date.dt.normalize()-d.order_estimated_delivery_date.dt.normalize()).dt.days
 extract=d.order_purchase_timestamp.max();cutoff=extract-pd.Timedelta(days=60);d['mature_60d']=d.order_purchase_timestamp.le(cutoff)
 local=ROOT/'data/processed';local.mkdir(exist_ok=True);d.to_parquet(local/'olist_order_grain.parquet',index=False)
 eligible=d[d.outcome_available];mature=eligible[eligible.mature_60d];state=segment(mature,'customer_state')
 baseline=float(mature.late.mean());state['late_count_above_pooled_reference']=state.late-state.delivered*baseline
 ranked=state[state.review_eligible].sort_values('late_count_above_pooled_reference',ascending=False);ranked.to_csv(P/'results/state_investigation.csv')
 cohorts=d.groupby('cohort').agg(all_orders=('order_id','size'),delivered_eligible=('outcome_available','sum'),late=('late','sum'),mature=('mature_60d','sum'));cohorts['late_rate_delivered_only']=cohorts.late/cohorts.delivered_eligible.replace(0,np.nan);cohorts['without_observed_eligible_delivery_fraction']=1-cohorts.delivered_eligible/cohorts.all_orders;cohorts.to_csv(P/'results/cohorts.csv')
 sensitivity=[]
 for days in [30,60,90]:
  pop=d[d.order_purchase_timestamp<=extract-pd.Timedelta(days=days)];e=pop[pop.outcome_available]
  sensitivity.append({'maturity_days_assumption':days,'all_orders':len(pop),'eligible_delivered':len(e),'late':int(e.late.sum()),'late_rate_delivered_only':float(e.late.mean()),'without_eligible_delivery':int((~pop.outcome_available).sum())})
 save(P/'results/metrics.json',{'grain_rows':len(d),'grain_unique':bool(d.order_id.is_unique),'extract_proxy':str(extract),'maturity_cutoff_60d':str(cutoff),'eligible_all_dates':len(eligible),'late_all_dates':int(eligible.late.sum()),'late_rate_delivered_only':float(eligible.late.mean()),'mature_eligible':len(mature),'mature_late':int(mature.late.sum()),'mature_rate':baseline,'maturity_sensitivity':sensitivity,'investigation_rule':'>=100 eligible delivered orders; rank excess late counts vs descriptive pooled reference; no causal interpretation','population_limit':'Undelivered and incomplete records excluded from late-rate denominator and reported separately. Extract proxy is latest purchase timestamp, not verified export timestamp.','license':'Olist CC BY-NC-SA 4.0. Noncommercial internal case study only.','environment':environment()})
 plt=configure_plot();top=ranked.head(10).sort_values('late_rate');fig,ax=plt.subplots();ax.barh(top.index,top.late_rate*100,color='#217c80');ax.errorbar(top.late_rate*100,top.index,xerr=np.array([top.late_rate-top.wilson_low,top.wilson_high-top.late_rate])*100,fmt='none',ecolor='black');ax.set(xlabel='Late deliveries among eligible delivered orders (%)',title='Olist: candidate segments for investigation, mature cohorts');fig.savefig(P/'figures/investigation.png');plt.close(fig)
 content=f'''<!doctype html><meta charset="utf-8"><title>Olist delivery review</title><style>body{{font:16px system-ui;max-width:1100px;margin:40px auto;color:#163443}}table{{border-collapse:collapse;width:100%}}td,th{{padding:10px;border-bottom:1px solid #ddd}}.warning{{background:#fff3cd;padding:18px}}</style><h1>Delivery reliability investigation</h1><p class="warning">Noncommercial study. Data: Olist, CC BY-NC-SA 4.0. Rates apply only to eligible delivered orders. Associations do not establish causes.</p><p>All-period late deliveries: {int(eligible.late.sum()):,} / {len(eligible):,} ({eligible.late.mean():.2%}). Mature cohort cutoff assumption: 60 days before {extract.date()}.</p><img width="100%" src="../figures/investigation.png" alt="Segment rates and Wilson intervals"><h2>Monthly cohorts, including incomplete delivery outcomes</h2>{cohorts.round(4).to_html()}<h2>Investigation queue</h2>{ranked.head(10).round(4).to_html()}<p>Review transport/process records before action. No seller sanctions, causal claim or commercial redistribution authorised.</p>'''
 (P/'results/dashboard.html').write_text(content,encoding='utf-8');print('PRJ3',len(d),'mature late rate',baseline,flush=True)
if __name__=='__main__':main()
