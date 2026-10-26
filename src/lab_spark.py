"""LAB2: Spark SQL, explicit schema, Parquet roundtrip and pandas parity."""
import os,zipfile,time,json,zlib,functools,operator
from pathlib import Path
import pandas as pd,numpy as np
from common import ROOT,WORK,project,save,environment
P=project('LAB2_pyspark')
def main():
 from pyspark.sql import SparkSession,functions as F,types as T
 data=ROOT/'data/processed/spark_input';data.mkdir(parents=True,exist_ok=True)
 # Sensor engineering complements alert research; no Olist NC material in this lab.
 with zipfile.ZipFile(ROOT/'data/raw/metro.zip') as z:
  member='MetroPT3(AirCompressor).csv';p=data/member
  if not p.exists():p.write_bytes(z.read(member))
  crc=0
  with p.open('rb') as f:
   while block:=f.read(1048576):crc=zlib.crc32(block,crc)
  assert crc==z.getinfo(member).CRC,'Cached Spark input differs from raw archive member'
 names=['TP2','TP3','H1','DV_pressure','Reservoirs','Oil_temperature','Motor_current','COMP','DV_eletric','Towers','MPG','LPS','Pressure_switch','Oil_level','Caudal_impulses']
 # Original CSV has a blank index header; "Unnamed: 0" is only pandas' display alias.
 schema=T.StructType([T.StructField('',T.LongType(),False),T.StructField('timestamp',T.StringType(),True)]+[T.StructField(n,T.DoubleType(),True) for n in names])
 builder=SparkSession.builder.master('local[2]').appName('DecisionReliabilityLAB2').config('spark.ui.enabled','false').config('spark.driver.bindAddress','127.0.0.1').config('spark.driver.host','127.0.0.1').config('spark.sql.shuffle.partitions','2')
 jar=WORK/'jars/hadoop-bare-naked-local-fs-0.1.0.jar'
 if os.name=='nt' and jar.exists():builder=builder.config('spark.jars',str(jar)).config('spark.driver.extraClassPath',str(jar)).config('spark.executor.extraClassPath',str(jar)).config('spark.hadoop.fs.file.impl','com.globalmentor.apache.hadoop.fs.BareLocalFileSystem')
 t=time.perf_counter();spark=builder.getOrCreate();spark.sparkContext.setLogLevel('ERROR')
 try:
  spark.conf.set('spark.sql.session.timeZone','UTC')
  d=spark.read.option('header',True).option('enforceSchema',False).option('mode','FAILFAST').schema(schema).csv(str(p)).withColumnRenamed('','row_id').withColumn('time',F.to_timestamp('timestamp'));rows=d.count()
  required=['row_id','time']+names;nulls=d.select(*[F.sum(F.col(c).isNull().cast('int')).alias(c) for c in required]).first().asDict();null=sum(int(v) for v in nulls.values());nonfinite=d.filter(functools.reduce(operator.or_,[F.isnan(c)|(F.abs(F.col(c))==float('inf')) for c in names])).count();dup=d.groupBy('row_id').count().filter('count>1').count();assert null==0 and dup==0 and nonfinite==0
  d.createOrReplaceTempView('sensors');sql="SELECT date_format(time,'yyyy-MM') AS month,COUNT(*) AS observations,AVG(TP2) AS mean_TP2,MIN(TP2) AS min_TP2,MAX(TP2) AS max_TP2 FROM sensors GROUP BY date_format(time,'yyyy-MM')";g=spark.sql(sql)
  output=ROOT/'data/processed/spark_sensor_parquet_javafs'
  # errorIfExists preserves prior output; an existing output is validated, never silently replaced.
  if not output.exists():g.coalesce(2).write.mode('errorifexists').parquet(str(output))
  back=spark.read.parquet(str(output));a=back.toPandas().sort_values('month').reset_index(drop=True)
  b=pd.read_csv(p,usecols=['timestamp','TP2']);b['month']=pd.to_datetime(b.timestamp).dt.strftime('%Y-%m');b=b.groupby('month').agg(observations=('TP2','size'),mean_TP2=('TP2','mean'),min_TP2=('TP2','min'),max_TP2=('TP2','max')).reset_index().sort_values('month').reset_index(drop=True)
  assert a.month.tolist()==b.month.tolist();assert np.array_equal(a.observations.to_numpy(),b.observations.to_numpy());assert np.allclose(a[['mean_TP2','min_TP2','max_TP2']],b[['mean_TP2','min_TP2','max_TP2']],rtol=1e-10,atol=1e-10)
  a.to_csv(P/'results/monthly_sensor_stats.csv',index=False)
  save(P/'results/metrics.json',{'engine_version':spark.version,'master':spark.sparkContext.master,'input_rows':rows,'null_required':null,'nulls_by_required_field':nulls,'nonfinite_sensor_rows':nonfinite,'cached_input_crc_matches_raw':True,'duplicate_row_ids':dup,'output_month_rows':len(a),'parquet_roundtrip':True,'pandas_parity_tolerance':1e-10,'elapsed_seconds':time.perf_counter()-t,'scale':'1516948 sensor rows on local[2]; no claim of big-data production experience','partitioning':'up to 2 physical output partitions; eight aggregate rows, directory partitioning adds no value','license':'MetroPT-3 CC BY 4.0, Davari et al.','environment':environment()});(P/'transform.sql').write_text(sql);print('LAB2 Spark/Parquet/pandas parity',rows,len(a),flush=True)
 finally:spark.stop()
if __name__=='__main__':main()
