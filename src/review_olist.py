"""Supplemental relational coverage review, using original public tables locally."""
from common import project,table,save
P=project('PRJ3_olist')
def main():
 tables={n:table('olist.zip',f'olist_{n}_dataset.csv') for n in ['orders','customers','order_items','order_payments','order_reviews','products','sellers','geolocation']}
 tables['translation']=table('olist.zip','product_category_name_translation.csv')
 keys={n:int(tables[n][key].duplicated().sum()) for n,key in [('orders','order_id'),('customers','customer_id'),('products','product_id'),('sellers','seller_id'),('translation','product_category_name')]}
 foreign={name:int((~tables[src][col].isin(tables[dst][key])).sum()) for name,src,col,dst,key in [('order_customer','orders','customer_id','customers','customer_id'),('item_order','order_items','order_id','orders','order_id'),('item_product','order_items','product_id','products','product_id'),('item_seller','order_items','seller_id','sellers','seller_id'),('payment_order','order_payments','order_id','orders','order_id'),('review_order','order_reviews','order_id','orders','order_id')]}
 assert not any(keys.values()) and not any(foreign.values())
 reviews=tables['order_reviews'];products=tables['products'];translation=tables['translation'];untranslated=products.product_category_name.notna()&~products.product_category_name.isin(translation.product_category_name)
 save(P/'results/relational_review.json',{'rows_by_table':{k:len(v) for k,v in tables.items()},'duplicate_primary_keys':keys,'foreign_key_orphans':foreign,'review_id_repeats':int(reviews.review_id.duplicated().sum()),'review_order_composite_repeats':int(reviews.duplicated(['review_id','order_id']).sum()),'products_without_category':int(products.product_category_name.isna().sum()),'products_with_untranslated_nonnull_category':int(untranslated.sum()),'geolocation_zip_is_unique':bool(tables['geolocation'].geolocation_zip_code_prefix.is_unique),'zip_prefix_types_preserved':{n:str(tables[n][c].dtype) for n,c in [('customers','customer_zip_code_prefix'),('sellers','seller_zip_code_prefix'),('geolocation','geolocation_zip_code_prefix')]},'interpretation':'Do not assume review_id or ZIP is a unique join key. Translation is optional and unmatched categories must remain visible.'})
 print('Olist relational review passed; untranslated products:',int(untranslated.sum()),flush=True)
if __name__=='__main__':main()
