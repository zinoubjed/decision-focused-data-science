import sys,pathlib,json,unittest,math
import numpy as np,pandas as pd
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from retail_production import features,evaluate
from metro_production import persistent,episodes
from cfpb_production import scrub,near_duplicate_mask
from common import wilson
class DecisionTests(unittest.TestCase):
 def test_retail_features_do_not_see_future(self):
  y=np.arange(110,dtype=float)+1;a=features(y,70);y[70:]=1e9;self.assertEqual(a,features(y,70))
 def test_constant_series_backtest(self):
  s=pd.Series(np.repeat(123.,104),index=pd.date_range('2009-12-13',periods=104,freq='W-SUN'));_,_,r=evaluate(s);self.assertAlmostEqual(r['seasonal_52']['MAE'],0)
 def test_missing_bin_breaks_alert(self):
  idx=pd.date_range('2020-01-01',periods=8,freq='10min');raw=pd.Series([True,True,False,True,True,True,True,False],index=idx);a=persistent(raw);self.assertEqual(int(a.sum()),2);self.assertEqual(episodes(a),[(idx[5],idx[6])])
 def test_private_pattern_scrubbing(self):
  text=scrub('Contact a.person@example.org on 212-555-1234 account 987654321');self.assertNotIn('@',text);self.assertNotIn('987654321',text);self.assertIn('PHONE',text)
 def test_template_guard(self):
  bad,_=near_duplicate_mask(['This is a completely identical complaint template'],['This is a completely identical complaint template','Orange bicycles are blue today']);self.assertEqual(bad.tolist(),[True,False])
 def test_wilson_nonzero_uncertainty(self):
  lo,hi=wilson(100,100);self.assertLess(lo,1);self.assertAlmostEqual(hi,1)
class ApiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from fastapi.testclient import TestClient
  from lab_api import app
  cls.client=TestClient(app)
 def test_health_and_request_id(self):
  r=self.client.get('/health');self.assertEqual(r.status_code,200);self.assertIn('x-request-id',r.headers)
 def test_real_forecast_endpoint(self):
  r=self.client.post('/forecast',json={'weekly_sales':list(range(1,105))});self.assertEqual(r.status_code,200);self.assertEqual(r.json()['forecast'],53)
 def test_reject_bad_shapes_and_values(self):
  for body in [{'weekly_sales':[1]*51},{'weekly_sales':[1]*261},{'weekly_sales':[-1]*52},{'weekly_sales':['private complaint']*52}]:self.assertEqual(self.client.post('/forecast',json=body).status_code,422)
 def test_nonfinite_validation(self):
  from lab_api import ForecastInput
  with self.assertRaises(ValueError):ForecastInput(weekly_sales=[float('nan')]*52)
if __name__=='__main__':unittest.main(verbosity=2)
