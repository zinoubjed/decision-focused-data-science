# Local API, Docker & CI Delivery

**LAB4 · LOCAL CONTAINER VERIFIED · portfolio project / local technical demonstration**

## Executive summary

Local unit/ASGI and HTTP tests passed. Actual Docker image build, loopback health/forecast/rejection, healthcheck and stop verified.

## Decision and scope

Deliver a finite-input numeric baseline API, test rejection paths, prepare container and CI, document rollback. Cloud not deployed. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

Authored numeric API and synthetic test fixtures; no private data or model weights in image. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/lab_api.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python -m unittest tests.test_api_ci -v
python -m uvicorn lab_api:app --app-dir src --host 127.0.0.1 --port 8000
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

Remote GitHub Actions and cloud deployment are not executed. Numeric synthetic fixtures only; no public endpoint or operational benefit claim.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** Local API, Docker & CI Delivery: evidence of method selection, data contracts, validation and transparent limits. Local unit/ASGI and HTTP tests passed. Actual Docker image build, loopback health/forecast/rejection, healthcheck and stop verified.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
