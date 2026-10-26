# Decision note after critical review

**STOP automatic routing.** The artifact remains useful as a historical NLP/triage study and an aid for human-verified suggestions. Neither 80.74% novel-test accuracy nor 91.39% accepted aggregate accuracy is a routing guarantee.

The global confidence threshold hides unequal outcomes by true category. Among accepted examples whose actual label is payday/title/personal loan, none of ten is correct; for student-loan examples only four of sixteen are correct. These are small, uncertain groups and cannot be identified by their true category at decision time. They must not be presented as a deployable class-specific safety policy. Full per-class coverage, counts and intervals are in selective_by_actual_class.json.

The earlier 1,506-review count covered only 4,677 retained novel test cases. The complete sampled workflow is 8,218 cases: 1,022 exact text repeats, 2,519 near repeats, and 1,506 novel low-confidence cases assigned to review. This gives 5,047 mandatory reviews and 3,171 accepted suggestions (38.59% of the original sampled test population). These are hypothetical processing rules, not measured staff workload or savings. Accepted suggestions also require human verification under the present recommendation.

Threshold choice used validation, not test labels; the new subgroup analysis does not retrofit thresholds on test. Wilson intervals during threshold search are descriptive and do not provide post-selection or drift guarantees. A future class-aware policy would need a new development protocol and fresh temporal evaluation, not selection from these test results.

At a hypothetical 25:1 wrong-suggestion-to-review cost, total cost units are 11,872 versus 8,218 for reviewing every sampled complaint. No business ROI is established. Costs, error severity, review rules, real routing labels and prospective drift evidence are missing. Preserve local-only text processing, abstention and human override.
