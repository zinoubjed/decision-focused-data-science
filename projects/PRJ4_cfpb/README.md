# Financial Complaint Triage & LLM Evaluation

**PRJ4 · PUBLICATION PACKAGE READY · portfolio project / local technical demonstration**

## Executive summary

Selected logistic_tfidf on validation macro-F1. Novel temporal test n=4,677: accuracy 80.74%, macro-F1 0.632, majority accuracy 54.12%. Threshold 0.6 has 273 wrong accepted suggestions; 1,506 low-confidence novel cases require review. Overall sampled workflow: 3,171/8,218 suggestions accepted (38.59%); 5,047 assigned to review including withheld text repeats.

## Decision and scope

Assist intake staff with consumer-product suggestions, abstention and human review. Product selection is a proxy, not institutional routing ground truth. Human override and abstention remain available. Business costs are unknown; hypothetical scenarios do not establish ROI.

## Source, rights and privacy

CFPB official Historical Narratives Archive; public reuse statement, no blanket CC assertion. Dataset audit evidence is preserved in `../../reports/`; decision contracts are in `../../docs/DECISION_CONTRACTS.md`. Original archives are immutable. Raw/processed data and local models live under ignored `data/` and are not publication assets.

## Method and data contract

See `docs/METHOD.md` and the executable source `../../src/cfpb_production.py`. Inputs, split boundaries, filtering rules and exact measurements are recorded in `results/metrics.json`. A successful command is an execution proof; it does not establish real-world deployment or personal independent mastery.

## Reproduce

From the portfolio root in the isolated environment, after acquiring authorised data:

```powershell
python src/cfpb_production.py
```

Versions: production `results/metrics.json` environment and `../../docs/REPRODUCIBILITY.md`. LAB1 requires local model assets; LAB2 requires Java; LAB3 requires TensorFlow. API tests on this Windows sandbox require loopback permission. No external model endpoint is used for complaint text.

## Tests and results

`../../reports/production_unit_tests.txt`, `../../reports/resume_integrity_tests.txt`, in-pipeline reconciliation assertions and the final artifact-validation journal distinguish executed tests from configuration alone. Outputs: JSON metrics, CSV tables and figures where relevant. Docker execution and remote CI are unverified unless their own run evidence exists.

## Decision note and limitations

No automatic routing recommended: aggregate accepted accuracy hides weak true-class outcomes. Results are on a 3% ID sample and template-filtered cohort. Character matching is not semantic deduplication. Confidence/Wilson search does not give a post-selection probability guarantee. Private text and vocabulary excluded; human-verification workflow required.

Next action: review the prepared publication content, rights and personal presentation before any external release.

## AI assistance and professional positioning

Codex produced code, analysis and editorial drafts and executed the recorded commands. The user has not been represented as independently executing these tasks. No seniority, client mission, economic gain, industrial deployment or personal skill validation is claimed.

**Recruiter summary.** Financial Complaint Triage & LLM Evaluation: evidence of method selection, data contracts, validation and transparent limits. Selected logistic_tfidf on validation macro-F1. Novel temporal test n=4,677: accuracy 80.74%, macro-F1 0.632, majority accuracy 54.12%. Threshold 0.6 has 273 wrong accepted suggestions; 1,506 low-confidence novel cases require review. Overall sampled workflow: 3,171/8,218 suggestions accepted (38.59%); 5,047 assigned to review including withheld text repeats.

**Client-facing method summary.** Demonstrates a bounded workflow and reviewable deliverables. Service availability and personal proficiency must be confirmed before offering paid work; this is not a client testimonial.

Publication drafts: `docs/PUBLICATION_KIT.md`. Nothing has been published.

## Local LLM diagnostic, not model selection

On the fixed balanced 54-case diagnostic, local FLAN-T5-small accuracy was 12.96%; TF-IDF on the same cases was 64.81%. All inference remained local; no complaint prompts or outputs were exported. See results/local_llm_diagnostic.json. This result does not estimate full-population accuracy.
