# Sensor-to-alert contract and event review

**Input and chronology.** Reuse the audit's prepared ten-minute medians, then calculate raw timestamp counts for coverage. A bin needs >=54 readings, a declared 90%-of-nominal-60 threshold. Median timestamps are shifted to bin close: the full bin cannot be used earlier. Missing or undercovered bins become invalid and break persistence. Raw timestamps remain naive; original timezone is unknown.

**Training and methods.** February is the only training period. Median/IQR scaling is training-only; zero IQR becomes one. Compare maximum absolute robust deviation with seeded 100-tree IsolationForest. Score quantiles .99/.995/.999 come from training only. The grid is a sensitivity, not selected on the four test reports. Three consecutive valid anomalous bins trigger an alert, and contiguous alert bins form one episode.

**Event contract.** Four original source windows: 18 April; 29–30 May; 5–7 June; 15 July 2020. Keep the duplicated event ID and maintenance-date ambiguity unresolved rather than fabricating corrections. Event overlap tests full episode intervals. Separately report any alert in the 24 hours before event onset and its earliest lead time. These alerts may be unrelated: anticipation flags do not establish predictive precursors.

**Exposure and false-alert limits.** Sum valid ten-minute bins into equivalent observed days; this excludes missing exposure and is not calendar uptime. Episodes outside every report window are unverified, not proven false positives. There is no complete label set for normal/failed operation. Report alert hours and review load alongside event overlap; sample-level accuracy is inappropriate.

**Decision.** Review suspicious regimes manually with operating-state and maintenance context. At .995, IsolationForest has fewer episodes than the sensor baseline, but the same small number of report windows does not establish superiority on future failures. No automatic shutdown, safety action, downtime reduction or operational predictive-maintenance claim is authorised.
