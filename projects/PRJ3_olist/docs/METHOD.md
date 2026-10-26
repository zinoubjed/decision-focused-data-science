# Relational contract and investigation note

**Grain.** Orders are unique by order_id. Customer lookup is many-to-one by customer_id; repeated real customers can have distinct order-level customer IDs. Items, payments and reviews are preaggregated separately before joining. Review means are descriptive post-outcome fields, never purchase-time features. No geolocation join is made on nonunique ZIP prefixes.

**SQL model.** `order_grain.sql` uses CTEs for item count/sellers/value/freight, payment count/value and review count/score, then left joins to orders. Row count and key uniqueness are asserted. The local analytical Parquet is under ignored data/processed, not a commercial publication asset.

**Population and denominator.** Late means the actual delivery calendar day exceeds the estimated calendar day. Eligible delivered orders need final delivered status and both dates. Undelivered orders, missing outcomes and late orders are counted separately. The overall 6.77% rate is conditional on 96,470 eligible delivered orders; it is not a 99,441-order reliability rate.

**Cohort maturity.** Exact extraction time is unknown; latest purchase timestamp is a proxy. The primary screen requires purchase at least 60 days before it, with 30/90-day sensitivity. This is not proof all remaining cohorts are fully resolved. Monthly tables expose all orders, eligible delivered orders, missing eligible-delivery fraction and maturity volume.

**Investigation queue.** For mature delivered orders, display state-level volume, count, rate and Wilson 95% intervals. Require >=100 observed delivered orders, then rank the excess late count over a pooled descriptive reference. This rule favours investigation volume, not causal blame or a statistically corrected discovery claim. Small cohorts are withheld from ranking. Customer-state association cannot establish seller or carrier responsibility.

**Action note.** For the leading segments, request transport legs, carrier capacity, promised-date revisions, holiday calendars and case-level explanations from an actual authorised operator before recommending changes. These missing data are not fabricated. Costs and benefits are unknown. A model is unnecessary for this retrospective decision.

**Rights.** Olist CC BY-NC-SA 4.0, official Kaggle version 2. Internal/noncommercial charts and derivatives retain attribution and applicable ShareAlike terms. Commercial-facing method descriptions must omit Olist-derived tables, metrics and graphics unless rights are clarified.
