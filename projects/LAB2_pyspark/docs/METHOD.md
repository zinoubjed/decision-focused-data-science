# Spark engineering contract

Input: 1,516,948 UCI MetroPT-3 observations from the original CSV, explicit row ID, timestamp string and 15 double sensor fields. Transform timestamp via Spark to_timestamp; set session UTC only for deterministic interpretation of naive time. Assert required time/TP2 values and row-ID uniqueness before aggregation.

Spark SQL produces month, observation count and TP2 mean/min/max. Genuine Spark writes Parquet; Spark reads it back. Pandas independently aggregates the original input; month keys and counts must match exactly, numeric summaries within rtol/atol 1e-10. Assertions fail before a success metrics file is written. Eight aggregate rows do not justify partitioned directory layout; two output files suffice.

Native Windows required a pure-Java filesystem adapter because default Hadoop local writes attempted Winutils. The adapter does not replace the Spark engine or Parquet writer. Its source, license and JAR hash are recorded. A successful output directory is never silently overwritten; reruns read and compare it to source. Initial failed output, if present, remains a separate directory.

Execution is local[2], not a production cluster or proof of large-scale industrial engineering. Record engine version, actual row count, elapsed time, parity and environment. Retain compatibility warnings: pandas >=3 is not fully supported by this Spark version, though the tested conversion and numerical parity passed.

**Critical review.** Cached input CRC must match the original ZIP member. FAILFAST parsing and strict header checking use the actual blank first header, then rename it to row_id; `Unnamed: 0` was a pandas-generated alias, not a source field. Required null checks now cover row_id, parsed time and all 15 sensors, and nonfinite sensors are checked separately. The existing Parquet output is compared to the current source calculation on every run.
