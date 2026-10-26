# Decision-Focused Data Scientist

Interpretable ML | Reliable Analytics

From imperfect data to defensible decisions.

This is an AI-assisted portfolio with recorded local execution. It does not assert seniority, client experience, industrial deployment or independently verified personal mastery.

## Selected decision studies

**Retail â€” an honest forecasting target.** Start with over a million imperfect transaction lines, distinguish positive observed sales from net revenue and latent demand, then compare temporal baselines and Ridge over identical origins. Retaining or removing ambiguous duplicate lines changes seasonal WAPE from 17.40% to 14.34%. The useful evidence is the cleaning sensitivity and the selection boundary, not a polished single score. Source: PRJ2 case study, chronological predictions and SQL reconciliation.

**Delivery reliability â€” grain before KPI.** A relational analysis keeps one row per order through independent item/payment/review aggregation. Cohort definitions expose incomplete outcomes; rates are conditional on delivered records, not the full order population. The commercial-facing presentation is method-only because Olist is CC BY-NC-SA 4.0. Source: PRJ3 SQL, tests, investigation note and noncommercial dashboard.

**Complaint intake â€” abstention with a measurable review queue.** Temporal, taxonomy and template controls precede model comparison. TF-IDF logistic accuracy is 80.74%, but macro-F1 is .632 and a rare class has weak recall. At the selected threshold, 273 wrong suggestions remain among 3,171 accepted cases. Hypothetical error costs can reverse the decision to automate. Local LLM inference performed poorly on its separate 54-case diagnostic; no sensitive text left the machine. The full sampled workflow has 5,047 reviews among 8,218 cases; subgroup harms preclude automatic routing. Source: PRJ4 class metrics, decision note, population flow and local LLM report.

**Sensor alerts â€” operational burden before headline recall.** Coverage-gated, bin-close features compare a simple robust baseline with IsolationForest. The evaluation counts episodes, observed exposure, report overlap and pre-event signals separately. Four event windows cannot establish prospective maintenance reliability. Source: PRJ5 episode table, threshold sensitivity and event review.

## Complementary technical evidence

- **RAG:** real local generation, source citations and baseline comparison, with explicit failures of a mechanical support guard and a scoring-alias review.
- **PySpark:** actual Spark SQL and Parquet on 1.52 million sensor observations, with independent pandas parity; local scale only.
- **TensorFlow:** three trained MLP initialisations, learning histories and a declared validation complexity hurdle that retains logistic regression.
- **Delivery:** API validation, ASGI and actual Docker build/run; healthcheck healthy, five invalid-input HTTP checks, non-root execution and clean stop. Remote CI/cloud unexecuted.

The evidence index is `../PRODUCTION_STATUS.md`; measured files and source are linked from `../production.html`. Thirty-two critical-review tests pass, supplemented by a fresh-tree 13-command recomputation and 40 substantive comparisons. Existing Telco work has been reproduced at a pinned GitHub commit: original 3 tests, 9 notebook cells and five report CSVs pass/match. Its original conclusions are preserved. Publication drafts require owner review and exact platform approval.
