# Decision contracts — WORKING, 23 October 2026

Decision Reliability > Model Performance. These are portfolio experiments produced with AI assistance. Personal autonomous proficiency is unverified. No CORE or educational status is changed.

## PRJ2 — PROMETTEUR, bounded operational planning

**Gate 0.** A planning analyst reviews next week's observed positive sales revenue at Sunday close. The available action is preparing a workload/revenue scenario, with human override and abstention if the extract is incomplete. No stock policy is inferred: inventory, stockouts, margin, staffing capacity and error costs are unavailable. Underforecast and overforecast costs remain assumptions, not ROI.

**DPD.** Chen, UCI Online Retail II, DOI 10.24432/C5CG6D, CC BY 4.0. One invoice line is not one order or customer. Audit both workbook sheets. Flag cancellations, nonpositive values, missing IDs and repeated rows separately. Target: positive recorded sales after an explicit cleaning rule; it excludes returns and is not net revenue or latent demand. Exact repeated lines may be legitimate; deduplication is an assumption requiring sensitivity analysis. Currency GBP; no inflation adjustment. One UK retailer, many wholesalers, 2009–2011: no contemporary market representativeness.

**Availability and validation.** Only completed weeks before the forecast origin are used. Remove the first and last incomplete weeks. One-week horizon. Compare last week, recent four-week average and annual seasonal baseline. Select on earlier origins, hold final 26 weeks out. Calendar shifts and exceptional stock adjustments may affect the target. Revenue aggregation and observed non-trading days are not proof of zero demand.

**MRT.** MAE in GBP and WAPE map to weekly absolute planning deviations. Report signed bias and interval coverage. A scenario interval is a review trigger, not a guaranteed probability statement. No automatic capacity purchase until real capacity and cost curves are supplied. Limited history precludes robust rare-event claims.

## PRJ3 — PROMETTEUR for retrospective diagnostics; commercial reuse restricted

**Gate 0.** An operations analyst selects delivery segments for investigation after delivery outcomes mature. Action: inspect processes and cohorts; never automatically sanction sellers or claim causation. Abstain for small or incomplete cohorts. Costs and service-level agreements unknown.

**DPD.** Olist's official Kaggle dataset, version 2; CC BY-NC-SA 4.0, verified via Kaggle API and stored in reports/olist_metadata.json. Preserve Olist attribution; transformed data remains subject to applicable ShareAlike terms. This case study is noncommercial. Do not repurpose its data/derivatives for paid offers without rights review. Order, item, payment, review and geolocation have different grains. Preaggregate many-side tables before joins. ZIP prefixes are identifiers; no individual geolocation is published.

**Availability.** Delivery timestamps, final status and reviews are retrospective outcomes. They are prohibited as purchase-time predictors. Estimated delivery date may be revised: its historical snapshot at purchase is not established. No predictive model is necessary. KPI denominator: delivered orders with actual and estimated delivery dates. A delivery is late when its calendar day exceeds the promised calendar day; date-only promises must not be treated as midnight deadlines. Undelivered orders are separately excluded and reported, preventing a misleading all-order reliability claim.

**MRT.** Report late counts, cohort volume, late rate and uncertainty, not ranking by rate alone. Require >=100 mature orders for exploratory segment review; this is a declared screening choice, not an optimal business threshold. A monthly cohort is immature near extract end. Unknown exposure and confounding forbid causal conclusions.

## PRJ4 — conditional PROMETTEUR after archive audit

**Gate 0.** A human intake reviewer receives a suggested broad consumer-product category from complaint text, with abstention. This simulates assistance; it does not reproduce a bank's actual routing. Wrong suggestions may delay review; errors have no known monetary cost. Human override is always available.

**DPD.** Use CFPB's official historical narratives exports, not the current narrative-free live database. CFPB states published complaint data is freely usable, analyzable and buildable; no blanket CC license is asserted. Archive page and link manifest establish provenance. Complaints are allegations and not a representative consumer sample. Product labels are consumer selections with taxonomy changes. Restrict initial experiment to May 2018–July 2023 taxonomy window. Never export raw text or claim redaction guarantees anonymity.

**Availability and leakage.** Text only as model input. Exclude response, company routing and post-submission metadata. Split chronologically (train before 2022, validation in 2022, test 2023 before August); deduplicate normalized text before splitting. Similar templates, explicit category words, repeat complainants and label ambiguity remain risks. Stable ID hash sampling is bounded and disclosed; it is not the full corpus evaluation. Report unseen/excluded classes.

**MRT.** Macro-F1 and per-class precision/recall reflect imbalance. Select a confidence threshold only on validation, requiring >=100 accepted and >=90% validation accuracy; if unavailable, abstain on all. Confidence is uncalibrated. Report accepted volume, wrong accepted suggestions and human review volume. Error costs 5/10/25 relative to unit review cost are sensitivities only. No LLM cost, latency or superiority result without an actual run.

## PRJ5 — PROMETTEUR for alert research; FAIBLE for predictive-maintenance claims

**Gate 0.** A maintenance analyst reviews persistent unusual sensor regimes. Decision at each completed 10-minute bin: inspect the alert or defer. No automatic train shutdown, repair or safety decision. Missed failures and inspection costs unknown. Missing bins suppress alerts and require a data-quality flag.

**DPD.** Davari et al., UCI MetroPT-3, DOI 10.24432/C5VW3R, CC BY 4.0. One sensor observation, one compressor, 2020. Original report intervals preserved: 18 April, 29–30 May, 5–7 June, 15 July. Duplicate event ID and inconsistent maintenance date in the source are not silently repaired. Anomaly scores are not failure labels. Source sampling descriptions conflict (1 Hz / 0.1 Hz); observed intervals govern processing.

**Availability and validation.** Ten-minute medians become available at bin close, not at its opening timestamp. Train IsolationForest and normalization on February only. Subsequent observations are evaluation data. Three consecutive anomalous bins form persistence; missing bins break the sequence. Evaluate a sensitivity grid of training-score quantiles; no best test threshold is selected. Include a simple sensor-range baseline before final review. Detecting during an event is not predicting it before onset.

**MRT.** Count alert episodes and alert hours, observed-day exposure, overlap with each report and 24-hour pre-event flags. Outside-report alerts are unverified, not ground-truth false positives. Four report windows cannot support a stable recall estimate or measured downtime reduction. Real operating procedures and prospective validation are needed for deployment.

## PRJ1 — Existing evidence reproduced

Existing repository at zinoubjed/telco-churn-portfolio reproduced at pinned commit d228c5712876c114954e566453f980f913fdab93. Three tests and nine notebook code cells pass; source results match. No reconstruction or external edits. Conditional historical ranking only; operational campaign STOP pending scoring time, target horizon, prospective representativeness, FP/FN costs and incremental intervention evaluation. No ROI, retention-gain or personal-mastery claim.
