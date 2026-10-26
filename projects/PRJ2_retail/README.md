# Retail Sales Forecasting & Operational Planning

**PRJ2 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

Validation selected seasonal_52. On 26 held-out one-week origins: MAE £40,170.66, WAPE 17.40%, signed bias £3,040.39. Separate interval evaluation: 61.54% coverage on 13 weeks. Exact-dedup seasonal WAPE 14.34% is a sensitivity, not a reason to alter the target.

## Decision and scope

Planning analyst reviews next week’s positive observed sales and uncertainty. No inventory, margin or latent-demand inference. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

UCI Online Retail II; Chen; DOI 10.24432/C5CG6D; CC BY 4.0. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/retail_production.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/retail_production.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

Thirteen selection weeks; 26 point-forecast test weeks split into 13 calibration and 13 interval-evaluation weeks. The nominal 90% scenario fails to achieve that coverage; no 90% reliability guarantee. Annual history is short and duplicates ambiguous. Mean-4 is better on this test, but no test-driven model switch is made. Costs are hypothetical.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** Retail Sales Forecasting & Operational Planning: evidence of method selection, data contracts, validation and transparent limits. Validation selected seasonal_52. On 26 held-out one-week origins: MAE £40,170.66, WAPE 17.40%, signed bias £3,040.39. Separate interval evaluation: 61.54% coverage on 13 weeks. Exact-dedup seasonal WAPE 14.34% is a sensitivity, not a reason to alter the target.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
