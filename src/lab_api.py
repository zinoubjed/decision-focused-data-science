"""LAB4 local numeric baseline API; never accepts complaint text or secrets."""
import logging,math,uuid,time
from fastapi import FastAPI,HTTPException,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,field_validator
logger=logging.getLogger('decision_api')
app=FastAPI(title='Observed Sales Baseline',version='1.0.0')
@app.exception_handler(RequestValidationError)
async def invalid_request(request:Request,exc:RequestValidationError):
 # Do not echo submitted values: NaN/Infinity cannot be serialized as JSON,
 # and input bodies do not belong in validation responses or request logs.
 return JSONResponse(status_code=422,content={'detail':[
  {'loc':list(e['loc']),'type':e['type'],'msg':'Invalid input'} for e in exc.errors()]})
class ForecastInput(BaseModel):
 weekly_sales:list[float]=Field(min_length=52,max_length=260)
 @field_validator('weekly_sales')
 @classmethod
 def finite_nonnegative(cls,v):
  if not all(math.isfinite(x) and 0<=x<=1e10 for x in v):raise ValueError('Sales must be finite, nonnegative and <=1e10')
  return v
@app.middleware('http')
async def audit_request(request:Request,call_next):
 start=time.perf_counter();response=await call_next(request);request_id=str(uuid.uuid4());response.headers['X-Request-ID']=request_id
 logger.info('request_id=%s method=%s path=%s status=%s elapsed_ms=%.2f',request_id,request.method,request.url.path,response.status_code,(time.perf_counter()-start)*1000)
 return response
@app.get('/health')
def health():return {'status':'ok','version':'1.0.0','deployment':'local demonstration'}
@app.post('/forecast')
def forecast(body:ForecastInput):
 return {'forecast':body.weekly_sales[-52],'horizon_weeks':1,'method':'seasonal_naive_52','n_history':len(body.weekly_sales),'limitations':'Requires complete chronological weeks. Positive observed sales only; no stock or ROI inference.'}
