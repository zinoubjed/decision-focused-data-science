import pathlib,json,hashlib,zipfile,unittest,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
class AuditEvidence(unittest.TestCase):
 def test_cfpb_complete_manifest(self):
  links=json.loads((ROOT/'reports/cfpb_links.json').read_text())
  integrity=json.loads((ROOT/'reports/cfpb_integrity.json').read_text())
  audit=json.loads((ROOT/'reports/cfpb_audit.json').read_text())
  self.assertEqual(len(links),21)
  expected={u.rsplit('/',1)[-1] for u in links}
  self.assertEqual({x['file'] for x in integrity},expected)
  self.assertEqual({x['archive'] for x in audit if x.get('status')=='OK' and x.get('audit_version')==2},expected)
  for x in integrity:
   p=ROOT/'data/raw'/x['file']
   self.assertEqual(p.stat().st_size,x['bytes'])
   with p.open('rb') as f: self.assertEqual(hashlib.file_digest(f,'sha256').hexdigest(),x['sha256'])
   self.assertIsNone(x['crc_error'])
 def test_duplicate_count_across_chunk_boundaries(self):
  sys.path.insert(0,str(ROOT/'src'))
  from cfpb import repeated_count
  seen=set()
  self.assertEqual(repeated_count(['a','a','b'],seen),1)
  self.assertEqual(repeated_count(['a','a','c','c'],seen),3)
  self.assertEqual(seen,{'a','b','c'})
 def test_cfpb_audited_archives_reconcile(self):
  p=ROOT/'reports/cfpb_audit.json'
  self.assertTrue(p.exists())
  d=json.loads(p.read_text())
  for x in d:
   if x.get('status')!='OK': continue
   self.assertEqual(x.get('audit_version'),2)
   self.assertIsNone(x['crc_error'])
   self.assertLessEqual(x['narratives'],x['rows'])
   self.assertEqual(sum(x['products'].values()),x['rows']-x['nulls']['Product'])
   self.assertEqual(sum(x['narrative_products'].values()),x['narratives']-x['narratives_missing_product'])
   self.assertLessEqual(x['duplicate_normalized_narratives'],x['narratives'])
 def test_original_archives(self):
  for r in json.loads((ROOT/'reports/acquisition.json').read_text()):
   if r['status']!='OK': continue
   p=ROOT/f"data/raw/{r['name']}.zip"
   with p.open('rb') as f: self.assertEqual(hashlib.file_digest(f,'sha256').hexdigest(),r['sha256'])
   with zipfile.ZipFile(p) as z: self.assertIsNone(z.testzip())
 def test_olist_denominator_and_join(self):
  d=json.loads((ROOT/'reports/olist_audit.json').read_text())
  n=d['tables']['olist_orders_dataset']['rows']
  self.assertEqual(d['sql_order_grain_rows'],n)
  self.assertEqual(d['delivery']['eligible']+d['delivery']['excluded'],n)
  self.assertTrue(all(x==0 for x in d['orphans'].values()))
  self.assertLessEqual(d['delivery']['late'],d['delivery']['eligible'])
 def test_metro_period_and_exposure(self):
  d=json.loads((ROOT/'reports/metro_audit.json').read_text())
  self.assertEqual(d['duplicate_timestamps'],0)
  self.assertEqual(sum(d['nulls'].values()),0)
  self.assertGreater(d['max_gap_seconds'],86400)
 def test_retail_sheet_reconciliation(self):
  d=json.loads((ROOT/'reports/retail_audit.json').read_text())
  self.assertEqual(sum(d['sheet_rows'].values()),d['rows'])
  self.assertLess(d['clean_rows'],d['rows'])
if __name__=='__main__': unittest.main(verbosity=2)
