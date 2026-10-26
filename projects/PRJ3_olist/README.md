# E-commerce Delivery Reliability Analytics

**PRJ3 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

SQL retained 99,441 unique orders. All-period late rate is 6,534/96,470 = 6.77%, conditional on eligible delivered orders. Mature 60-day cohort rate: 6.85%.

## Decision and scope

Operations analyst prioritises delivery segments for investigation after outcomes mature. No purchase-time prediction or causal sanction. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

Olist official Kaggle v2; CC BY-NC-SA 4.0; noncommercial only. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/olist_production.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/olist_production.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

Noncommercial Olist restriction. Undelivered orders are outside the late-rate denominator and explicitly counted. Export date is not known; latest purchase is a proxy, with 30/60/90-day maturity sensitivities. Wilson intervals assume independent Bernoulli outcomes; repeat-customer/route dependence and confounding remain.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** E-commerce Delivery Reliability Analytics: evidence of method selection, data contracts, validation and transparent limits. SQL retained 99,441 unique orders. All-period late rate is 6,534/96,470 = 6.77%, conditional on eligible delivered orders. Mature 60-day cohort rate: 6.85%.

**Client-facing method summary.** Noncommercial case study only. Describe grain, joins, cohort definitions and quality checks without redistributing Olist-derived metrics, visuals or data into commercial offers.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
