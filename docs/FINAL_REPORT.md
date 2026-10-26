> Technical evidence snapshot from 23 October 2026. Publication and code-licence status is superseded by ../PUBLICATION_STATUS.md and ../LICENSING.md; measurements and their limits remain unchanged.

# Production coverage — updated after critical review, 23 October 2026



Current authority: **CRITICAL_REVIEW.md** and REPRODUCTION_RUNBOOK.md. The pre-review archive is retained privately. Material interval/workload/scoring conclusions have been corrected; see the dedicated review.



The user authorised PRJ2–PRJ5 and LAB1–LAB4 after reviewing the four dataset audits. Those audits were reused; original ZIPs, SHA-256/CRC evidence and dated reports are preserved. The pedagogical CORE remains WORKING and unchanged.



Eight realizations (four new projects, three model/data labs and the existing Telco project) have executed computations, meaningful tests, measured outputs, reviewed figures where applicable, case-study documentation, reproducibility instructions, AI disclosure and prepared publication drafts. LAB4 now also has a real built/run container, five invalid-input checks, healthy healthcheck, non-root execution and clean stop. All nine realizations have bounded local execution evidence. PRJ1 existing project has now been reproduced without changing its conclusions.



| Item | Work and measured result | Limits / technical status / next action |

|---|---|---|

| PRJ1 Telco | Existing pinned GitHub project reproduced in its original locked Python environment: 3 tests, 9 notebook code cells, 5 CSV comparisons and identical full summary; AUC .8433, top30 423/246 | Existing evidence verified; two Notion pages consistent, no external edits. Historical educational ranking; no campaign benefit or deployment. See projects/PRJ1_telco/README.md |

| PRJ2 Retail | Positive observed sales; duplicate/return sensitivity; four forecasting approaches; 13 validation origins and 26 held-out one-week forecasts; validation-selected seasonal baseline WAPE 17.40%, MAE £40,170.66; exact-dedup sensitivity WAPE 14.34%; SQL total reconciliation; interval coverage 61.54% on 13 evaluation weeks after a disjoint 13-week calibration block | PUBLICATION PACKAGE READY within bounded historical scope. Duplicates are ambiguous, history short, scenarios broad. Mean-4 is better on this test, but no retrospective model switch. No stock/latent-demand/ROI claim |

| PRJ3 Olist | Advanced CTE aggregation preserves 99,441 unique orders; local order-grain Parquet, cohort/maturity sensitivity, Wilson intervals and dashboard; 6,534/96,470 eligible delivered orders late (6.77%); 60-day mature cohort rate 6.85% | PUBLICATION PACKAGE READY for noncommercial case study. Denominator excludes undelivered/incomplete outcomes. Cohort extraction date is a proxy. No causal blame or commercial derivative reuse |

| PRJ4 CFPB | 3% deterministic ID sample, 115,731 narratives sampled from all 21 exports; stable taxonomy window; exact and character-near-duplicate controls; train 16,463, validation 7,464, test 4,677; TF-IDF logistic macro-F1 .632, accuracy 80.74%, majority 54.12%; threshold .6 accepts 3,171 with 273 wrong, 1,506 reviews within the novel cohort; full sampled workflow 5,047/8,218 reviews, 38.59% accepted suggestions; accepted aggregate accuracy 91.39% | PUBLICATION PACKAGE READY for historical human-verified suggestions. Automatic routing is refused; rare-class accepted outcomes and recall are weak; confidence uncalibrated; template-filtered cohort not population performance. Private text/model/vocabulary excluded. Local LLM diagnostic is tiny and not a deployment comparison |

| PRJ5 MetroPT-3 | Ten-minute medians, >=54 raw readings/bin, bin-close availability, first-month training, 3-bin persistence; robust range vs IsolationForest; at quantile .995, 175 vs 30 episodes, IF 23 episodes outside reports, 142.16 equivalent valid days; overlaps 4/4 reports but prior-24h flag only 1/4 | PUBLICATION PACKAGE READY as alert-reliability research. Outside-report alerts unverified, not proven false positives. One machine/four windows, no prospective safety or maintenance benefit |

| LAB1 RAG | Eight fictional policy documents, SVD embeddings, local pinned FLAN-T5, 20 fixed questions, citations, baseline and guard; raw correctness 70%, guarded 85%; original automatic baseline substring 0%, explicit exact-alias rubric-v2 baseline 10%; explicit failure/citation review | PUBLICATION PACKAGE READY as an evaluation demonstration. Source-substring guard still accepts irrelevant copied phrases. AI inspection is not independent human assessment. No unattended assistant claim |

| LAB2 PySpark | Real Spark 4.2.0 local[2], explicit 17-field schema, 1,516,948 sensor rows, SQL monthly aggregation, real Spark Parquet write/read, eight monthly rows, pandas parity at 1e-10 | PUBLICATION PACKAGE READY as local engineering proof. Pure-Java filesystem adapter resolves Windows Winutils issue. Pandas-3 compatibility warning retained; tested conversion passed. No production-cluster claim |

| LAB3 TensorFlow | Real TensorFlow 2.21 CPU, 6,570-parameter MLP, three initialisation seeds; 1,078/359/360 split; test accuracies 97.22%, 96.67%, 96.94%; logistic 96.39%; mean validation MLP improvement below declared +1-point complexity hurdle | PUBLICATION PACKAGE READY as benchmark. Logistic retained by validation rule. Not writer-disjoint; shared split across seeds. Windows runtime omits only unused custom-op C++ headers, no registry change |

| LAB4 Delivery | Numeric FastAPI endpoint, input bounds/nonfinite checks, request IDs and body-free logging; real loopback HTTP health/forecast/rejection passed; Dockerfile, health check, restricted build context, CI and rollback prepared | LOCAL CONTAINER VERIFIED: Docker Desktop 4.96.3, WSL 3.0.3 and engine 29.9.2. Health/forecast 200, five rejection cases 422, healthcheck healthy, UID1000 and clean stop. Remote CI/cloud unexecuted |



## Tests and reviews



`reports/final_tests.txt` preserves the initial 26-test run; `reports/critical_review_tests.txt` records **32 tests executed and passed**, covering original archive integrity, all 21 CFPB exports, count reconciliation, duplicate-counter regression, forecast feature timing, constant-series reference, missing-bin persistence, privacy-pattern filtering, template guard, statistical interval uncertainty, actual ASGI health/forecast/rejection, private-output population counts, real Spark Parquet, TensorFlow history and RAG failure/refusal evidence.



In-pipeline assertions additionally verify SQL totals, key uniqueness, temporal splits, no exact train/evaluation text overlap and Spark/pandas parity. `reports/spark_execution.txt` records the successful engine run. `projects/LAB4_delivery/results/local_http.log` records local server requests and shutdown. Figures were visually inspected; the CFPB confusion plot was revised to show class-normalized values and legible labels. RAG scoring aliases and citation failures were reviewed explicitly without altering preserved automatic measurements.



The local LLM complaint diagnostic evaluates the first six retained test cases per class, 54 total. It is balanced, small and truncated. FLAN-T5 accuracy is 12.96%; TF-IDF accuracy on the same 54 cases is 64.81%; the full comparison is in `projects/PRJ4_cfpb/results/local_llm_diagnostic.json`. No complaint text, prompt, output or ID was transmitted to a model API or exported in reports. No model choice is made from this diagnostic.



## Reproduction and outputs



Start with `production.html`, `PRODUCTION_STATUS.md`, `reports/production_current.csv`, each project README, and `docs/REPRODUCIBILITY.md`. Production source is under src/, raw and private intermediate files under ignored data/. Each metrics JSON records the executing environment. Reproduction commands do not rebuild the audits from scratch. Third-party licenses and limits are registered in ATTRIBUTIONS.md.



## Professional positioning and publication



Decision-Focused Data Scientist | Interpretable ML | Reliable Analytics.



From imperfect data to defensible decisions.



Each realization has a recruiter-oriented case study and platform-specific editorial drafts. Client-facing material describes bounded deliverables and does not create an offer, invent service availability, claim seniority or imply real client outcomes. Olist commercial-facing copy is method-only. No personal autonomous proficiency is marked verified.



No new GitHub repository, Notion page, Kaggle submission, public site, social post, freelance offer or application has been published by this work. Existing Telco GitHub and Notion artifacts were read only. No cloud service or spend has been authorised or provisioned. External release still needs exact platform/content approval, rights review and owner choice of code licence. The prepared archive is a private review package, not an assertion that every asset may be commercially redistributed.



## Concrete remaining dependencies



1. PRJ1 access dependency resolved; original code licence remains an owner decision.

2. Docker/LAB4 dependency resolved locally. Remote CI and cloud remain unexecuted; they are not implied by local completion.

3. Exact publication content/platform approval after review; no generic credential request and no secrets in chat.



All independent production and preparation work has proceeded despite these dependencies. Decision Reliability > Model Performance.





## Additional critical-review proof



A fresh extracted computation snapshot completed 13 commands with copied frozen raw inputs and no prepared cache; 40 substantive comparisons passed. Existing runtimes/assets were reused, and later bounded helper/editorial differences are disclosed. Seven companion notebooks were executed locally; no Kaggle run is claimed. Current concrete channel drafts and release allowlists are described in CRITICAL_REVIEW.md.





## Connection and Docker completion — 23 October 2026



PRJ1 original code/results and two Notion pages were audited read only; no reconstruction or external edits. Docker official installer signature/hash verified, Windows prerequisites activated with user approval, manual reboot confirmed, WSL installed, real container built/tested/stopped. A NaN validation-response failure found during actual container testing was corrected and regression-tested. See LAB4 results/container_smoke.json and docs/METHOD.md. GitHub/Notion connected evidence was read; Upwork connection had been confirmed by coordination, with no profile, offer or application change.



Current post-Docker verification: **33 tests passed** (reports/post_docker_tests.txt), including a new nonfinite wire-input response regression and assertions on recorded container execution. The original 32-test journal and fresh 13-command/40-comparison snapshot remain preserved; the API fix is subsequent work and was tested separately. Original Telco additionally passed its three own tests and nine full computation notebook cells in its separate original runtime.

