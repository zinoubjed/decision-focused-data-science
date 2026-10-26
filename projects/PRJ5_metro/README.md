# Industrial Anomaly Detection & Alert Reliability

**PRJ5 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

At training quantile .995: IsolationForest 30 episodes versus robust baseline 175; 23 IF episodes do not overlap reports. Overlap in 4/4 report windows; prior-24h alerts in 1/4. Valid exposure 142.16 equivalent days.

## Decision and scope

Maintenance analyst reviews persistent unusual regimes. No automated safety action, downtime-reduction or operational maintenance claim. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

UCI MetroPT-3; Davari et al.; DOI 10.24432/C5VW3R; CC BY 4.0. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/metro_production.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/metro_production.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

One compressor and four documented windows. No full false-positive ground truth: outside-report episodes are unverified. Threshold grid is a sensitivity, not test tuning. Bins need >=54 observations and are available at closing time; 3-bin persistence. Prior alerts may be unrelated; no causal precursor or maintenance benefit claim.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** Industrial Anomaly Detection & Alert Reliability: evidence of method selection, data contracts, validation and transparent limits. At training quantile .995: IsolationForest 30 episodes versus robust baseline 175; 23 IF episodes do not overlap reports. Overlap in 4/4 report windows; prior-24h alerts in 1/4. Valid exposure 142.16 equivalent days.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
