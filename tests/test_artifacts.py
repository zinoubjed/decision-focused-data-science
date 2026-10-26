import pathlib,json,unittest
import pandas as pd
ROOT=pathlib.Path(__file__).resolve().parents[1];P=ROOT/'projects'
def get(name):return json.loads((P/name/'results/metrics.json').read_text())
class ExecutedArtifacts(unittest.TestCase):
 def test_retail_holdout_and_sensitivity(self):
  m=get('PRJ2_retail');self.assertEqual(len(m['variants']),2)
  d=pd.read_csv(P/'PRJ2_retail/results/backtest_retain_ambiguous_duplicates.csv')
  self.assertTrue((pd.to_datetime(d.origin_end)<pd.to_datetime(d.target_end)).all());self.assertEqual(d.model.nunique(),4)
  for x in m['variants'].values():self.assertEqual(x['test_origins'],26);self.assertEqual(x['validation_origins'],13)
  self.assertTrue(json.loads((P/'PRJ2_retail/results/sql_check.json').read_text())['passed'])
 def test_olist_population_reconciliation(self):
  m=get('PRJ3_olist');c=pd.read_csv(P/'PRJ3_olist/results/cohorts.csv')
  self.assertEqual(int(c.all_orders.sum()),m['grain_rows']);self.assertEqual(int(c.delivered_eligible.sum()),m['eligible_all_dates']);self.assertEqual(int(c.late.sum()),m['late_all_dates'])
  self.assertTrue((c.late<=c.delivered_eligible).all());self.assertEqual(len(m['maturity_sensitivity']),3)
 def test_cfpb_review_and_confusion(self):
  m=get('PRJ4_cfpb');c=pd.read_csv(P/'PRJ4_cfpb/results/confusion.csv',index_col=0)
  self.assertEqual(int(c.to_numpy().sum()),m['test']);self.assertEqual(m['accepted']+m['human_review'],m['test']);self.assertLessEqual(m['accepted_wrong'],m['accepted']);self.assertGreater(m['test_macro_f1'],0)
  self.assertEqual(m['validation']+m['near_validation_removed'],m['validation_before_near_filter']);self.assertEqual(m['test']+m['near_test_removed'],m['test_before_near_filter'])
 def test_metro_exposure(self):
  m=get('PRJ5_metro');self.assertEqual(len(m['results']),6)
  for x in m['results']:
   self.assertEqual(len(x['event_windows']),4);self.assertEqual(x['valid_bins']+m['test_invalid_bins'],m['test_bins']);self.assertLessEqual(x['episodes_no_overlap_report'],x['episodes'])
  self.assertTrue(m['no_false_positive_ground_truth'])
 def test_rag_diagnostic_and_refusals(self):
  m=get('LAB1_rag');d=json.loads((P/'LAB1_rag/results/evaluation_rows.json').read_text());self.assertEqual(len(d),m['questions']);self.assertEqual(m['external_api_calls'],0)
  self.assertTrue(any(x['guard_abstained'] for x in d));self.assertTrue(any(not x['guarded_correct'] and not x['guard_abstained'] for x in d));self.assertTrue((P/'LAB1_rag/docs/FAILURE_REVIEW.md').exists())
 def test_real_spark_parquet(self):
  m=get('LAB2_pyspark');self.assertEqual(m['input_rows'],1516948);self.assertTrue(m['parquet_roundtrip']);files=list((ROOT/'data/processed/spark_sensor_parquet_javafs').glob('*.parquet'));self.assertTrue(files)
  d=pd.concat([pd.read_parquet(f) for f in files]);self.assertEqual(int(d.observations.sum()),m['input_rows']);self.assertEqual(len(d),8)
 def test_tensorflow_training_and_rule(self):
  m=get('LAB3_tensorflow');self.assertEqual(sum(m['split_sizes'].values()),1797);self.assertEqual(len(m['tensorflow_runs']),3)
  for x in m['tensorflow_runs']:self.assertGreater(x['epochs'],1);self.assertEqual(x['parameters'],6570);self.assertGreater(x['fit_seconds'],0)
  expected='tensorflow_mlp' if m['validation_mean_network_accuracy']>=m['baseline']['validation_accuracy']+.01 else 'logistic_regression';self.assertEqual(m['retained'],expected)
 def test_real_api_and_container_execution_evidence(self):
  m=get('LAB4_delivery');self.assertEqual(m['forecast_http'],200);self.assertEqual(m['invalid_input_http'],422);self.assertFalse(m['public_listener'])
  c=json.loads((P/'LAB4_delivery/results/container_smoke.json').read_text())
  self.assertTrue(c['verified']);self.assertTrue(c['stopped']);self.assertEqual(c['exit_code'],0)
  self.assertEqual(c['healthcheck']['Status'],'healthy');self.assertNotEqual(c['nonroot_uid'],'0')
  self.assertEqual(c['port_bindings']['8000/tcp'][0]['HostIp'],'127.0.0.1')
  self.assertEqual(len(c['invalid_cases']),5);self.assertTrue(all(x['http']==422 for x in c['invalid_cases']))
  self.assertFalse((P/'LAB4_delivery/results/blocker.json').exists())
if __name__=='__main__':unittest.main(verbosity=2)
