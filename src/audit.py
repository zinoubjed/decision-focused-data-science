"""Reproducible audit. No raw archive is extracted or changed."""
import pathlib, json, zipfile, pandas as pd, numpy as np, sqlite3
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'reports'; OUT.mkdir(exist_ok=True)
def save(name,obj): (OUT/f'{name}.json').write_text(json.dumps(obj,indent=2,default=str),encoding='utf-8')
def quality(d):
 return {'rows':len(d),'columns':list(d.columns),'dtypes':d.dtypes.astype(str).to_dict(),'nulls':d.isna().sum().astype(int).to_dict(),'duplicate_rows':int(d.duplicated().sum())}
def olist():
 with zipfile.ZipFile(ROOT/'data/raw/olist.zip') as z:
  tables={n.removesuffix('.csv'):pd.read_csv(z.open(n)) for n in z.namelist() if n.endswith('.csv')}
 result={'tables':{k:quality(v) for k,v in tables.items()}}
 o=tables['olist_orders_dataset']; c=tables['olist_customers_dataset']; i=tables['olist_order_items_dataset']; p=tables['olist_order_payments_dataset']; r=tables['olist_order_reviews_dataset']
 result['keys']={'orders_duplicate_order_id':int(o.order_id.duplicated().sum()),'customers_duplicate_customer_id':int(c.customer_id.duplicated().sum()),'item_composite_duplicates':int(i.duplicated(['order_id','order_item_id']).sum()),'payment_composite_duplicates':int(p.duplicated(['order_id','payment_sequential']).sum()),'review_repeated_order':int(r.order_id.duplicated().sum())}
 result['orphans']={k:int((~v.order_id.isin(o.order_id)).sum()) for k,v in [('items',i),('payments',p),('reviews',r)]}
 result['orders_missing_customers']=int((~o.customer_id.isin(c.customer_id)).sum())
 for col in o.columns:
  if col.endswith('_at') or col.endswith('_date') or col=='order_purchase_timestamp': o[col]=pd.to_datetime(o[col],errors='coerce')
 result['period']=[str(o.order_purchase_timestamp.min()),str(o.order_purchase_timestamp.max())]
 result['status']=o.order_status.value_counts().to_dict()
 eligible=o[(o.order_status=='delivered') & o.order_delivered_customer_date.notna() & o.order_estimated_delivery_date.notna()].copy()
 # Compare calendar days: the promised deadline is a date, not midnight delivery.
 eligible['late_days']=(eligible.order_delivered_customer_date.dt.normalize()-eligible.order_estimated_delivery_date.dt.normalize()).dt.days
 eligible['late']=eligible.late_days.gt(0)
 result['delivery']={'eligible':len(eligible),'excluded':len(o)-len(eligible),'late':int(eligible.late.sum()),'late_rate':float(eligible.late.mean()),'purchase_after_delivery':int((eligible.order_delivered_customer_date<eligible.order_purchase_timestamp).sum())}
 joined=eligible.merge(c[['customer_id','customer_state']],on='customer_id',validate='many_to_one')
 state=joined.groupby('customer_state').agg(orders=('order_id','size'),late=('late','sum')); state['rate']=state.late/state.orders
 state.to_csv(OUT/'olist_delivery_by_state.csv')
 monthly=joined.groupby(joined.order_purchase_timestamp.dt.to_period('M').astype(str)).agg(orders=('order_id','size'),late=('late','sum')); monthly['late_rate']=monthly.late/monthly.orders; monthly.to_csv(OUT/'olist_delivery_month.csv')
 db=sqlite3.connect(':memory:')
 for name,d in [('orders',o),('items',i),('payments',p)]: d.to_sql(name,db,index=False)
 sql='''WITH items_by_order AS (SELECT order_id,COUNT(*) AS items,SUM(price) AS value FROM items GROUP BY order_id), payments_by_order AS (SELECT order_id,SUM(payment_value) AS paid FROM payments GROUP BY order_id) SELECT o.order_id,o.order_status,COALESCE(i.items,0) AS items,i.value,p.paid FROM orders o LEFT JOIN items_by_order i USING(order_id) LEFT JOIN payments_by_order p USING(order_id)'''
 (ROOT/'src/olist_order_grain.sql').write_text(sql,encoding='utf-8'); order_grain=pd.read_sql_query(sql,db)
 assert len(order_grain)==len(o) and order_grain.order_id.is_unique
 result['sql_order_grain_rows']=len(order_grain)
 result['naive_join_rows']=int(pd.read_sql_query('SELECT COUNT(*) AS n FROM orders JOIN items USING(order_id) JOIN payments USING(order_id)',db).iloc[0,0])
 save('olist_audit',result); print('olist',result['delivery'],flush=True)
def retail():
 with zipfile.ZipFile(ROOT/'data/raw/retail.zip') as z:
  n=next(n for n in z.namelist() if n.endswith('.xlsx')); sheets=pd.read_excel(z.open(n),sheet_name=None,engine='openpyxl')
 d=pd.concat(sheets.values(),ignore_index=True); result=quality(d); result['sheet_rows']={k:len(v) for k,v in sheets.items()}
 d.columns=['invoice','stock','description','quantity','date','price','customer','country']
 d['date']=pd.to_datetime(d.date); cancel=d.invoice.astype(str).str.upper().str.startswith('C')
 result.update(period=[str(d.date.min()),str(d.date.max())],cancellations=int(cancel.sum()),nonpositive_quantity=int(d.quantity.le(0).sum()),nonpositive_price=int(d.price.le(0).sum()))
 clean=d[~cancel & d.quantity.gt(0) & d.price.gt(0)].drop_duplicates().copy(); clean['revenue']=clean.quantity*clean.price
 result['clean_rows']=len(clean)
 # Explicit positive-sales target, not net sales or latent demand. Exclude incomplete edge weeks.
 s=clean.set_index('date').revenue.resample('W-SUN').sum().iloc[1:-1]
 s.to_csv(OUT/'retail_weekly.csv'); result['complete_weeks']=len(s)
 save('retail_audit',result); print('retail',len(d),flush=True)
def metro():
 with zipfile.ZipFile(ROOT/'data/raw/metro.zip') as z:
  d=pd.read_csv(z.open(next(n for n in z.namelist() if n.endswith('.csv'))))
 result=quality(d); t=pd.to_datetime(d.timestamp); delta=t.diff().dt.total_seconds()
 result.update(period=[str(t.min()),str(t.max())],duplicate_timestamps=int(t.duplicated().sum()),nonpositive_intervals=int(delta.le(0).sum()),interval_counts=delta.value_counts().head(15).to_dict(),gaps_over_10s=int(delta.gt(10).sum()),max_gap_seconds=float(delta.max()))
 s=d.drop(columns=[c for c in d if c=='timestamp' or c.startswith('Unnamed') or c=='index']).set_index(t).resample('10min').median()
 s.to_csv(OUT/'metro_10min.csv'); save('metro_audit',result); print('metro',len(d),flush=True)
if __name__=='__main__':
 for name,fn in [('olist',olist),('retail',retail),('metro',metro)]:
  if (ROOT/f'data/raw/{name}.zip').exists(): fn()
