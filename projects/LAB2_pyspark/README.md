# PySpark Sensor Data Engineering

**LAB2 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

Spark 4.2.0, local[2]: 1,516,948 sensor rows, 8 monthly aggregates. Spark Parquet roundtrip and pandas parity passed at tolerance 1e-10. Elapsed 21.04s.

## Decision and scope

Verify typed distributed transformations, Spark SQL and Parquet against pandas on one local machine. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

UCI MetroPT-3, CC BY 4.0, Davari et al.; PySpark Apache-2.0. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/lab_spark.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/lab_spark.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

Local scale only. Timezone setting is computational normalization of naive timestamps, not evidence of original UTC. Monthly aggregation has only eight output rows; two files are sufficient and directory partitioning adds no value.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** PySpark Sensor Data Engineering: evidence of method selection, data contracts, validation and transparent limits. Spark 4.2.0, local[2]: 1,516,948 sensor rows, 8 monthly aggregates. Spark Parquet roundtrip and pandas parity passed at tolerance 1e-10. Elapsed 21.04s.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
