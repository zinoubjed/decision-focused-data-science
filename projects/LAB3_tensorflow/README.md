# TensorFlow vs Classical Baseline Benchmark

**LAB3 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

Held-out digits test: logistic accuracy 96.39%; TensorFlow seed accuracies 97.22%, 96.67%, 96.94%. Retained by validation complexity rule: logistic_regression.

## Decision and scope

Test a CPU Keras MLP against logistic regression; retain complexity only when validation supports it. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

scikit-learn bundled UCI optical digits; cite original creators E. Alpaydin and C. Kaynak and sklearn load_digits; no images redistributed. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/lab_tensorflow.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/lab_tensorflow.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

Small 8×8-image benchmark, not an industrial task. Split is stratified by image, not writer-disjoint; writer dependence cannot be excluded. Three initialisation seeds share one test set. CPU timings are environment-specific; reduced Windows runtime omits only custom-op C++ headers.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** TensorFlow vs Classical Baseline Benchmark: evidence of method selection, data contracts, validation and transparent limits. Held-out digits test: logistic accuracy 96.39%; TensorFlow seed accuracies 97.22%, 96.67%, 96.94%. Retained by validation complexity rule: logistic_regression.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
