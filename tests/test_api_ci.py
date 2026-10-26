import sys,pathlib,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'src'))
from fastapi.testclient import TestClient
from lab_api import app
class ApiCI(unittest.TestCase):
 def test_health_forecast_and_rejection(self):
  c=TestClient(app);self.assertEqual(c.get('/health').status_code,200)
  r=c.post('/forecast',json={'weekly_sales':[10]*52});self.assertEqual(r.json()['forecast'],10)
  self.assertEqual(c.post('/forecast',json={'weekly_sales':[-1]*52}).status_code,422)
 def test_nonfinite_wire_values_return_422_without_echo(self):
  c=TestClient(app)
  for value in ['NaN','Infinity','-Infinity','1e999']:
   with self.subTest(value=value):
    r=c.post('/forecast',content='{"weekly_sales":['+','.join([value]*52)+']}',headers={'Content-Type':'application/json'})
    self.assertEqual(r.status_code,422)
    self.assertNotIn('input',r.json()['detail'][0])
    self.assertIn('X-Request-ID',r.headers)
if __name__=='__main__':unittest.main()
