# RAG & Local Generative AI Evaluation

**LAB1 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

Local FLAN-T5-small, 20 fixed questions. Explicit post-run rubric v2: raw RAG 70%, guarded 85%, no-RAG 10%; reference-document precision 83.33%. Original substring baseline score 0% is preserved but is not the semantic headline.

## Decision and scope

Evaluate source retrieval, local generation, abstention and failure modes on a fixed diagnostic set. Not a production knowledge assistant. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

Authored fictional Lumen Library policies; corpus CC0-1.0; FLAN-T5-small Apache-2.0. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/lab_rag.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/lab_rag.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

Tiny authored set, post-run rubric clarification, no blind human evaluation. Document matches are not citation entailment. The guard still accepts irrelevant copied phrases. 7-D SVD vectors are latent-semantic, not neural. Zero API charge excludes hardware/electricity. Not suitable for unattended use.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** RAG & Local Generative AI Evaluation: evidence of method selection, data contracts, validation and transparent limits. Local FLAN-T5-small, 20 fixed questions. Explicit post-run rubric v2: raw RAG 70%, guarded 85%, no-RAG 10%; reference-document precision 83.33%. Original substring baseline score 0% is preserved but is not the semantic headline.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.
