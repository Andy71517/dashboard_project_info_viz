# Updated datasheet summary after Round 1

**Data.** Census HPS 2024 Cycles 1–9 supplies 610,755 adult response records, analyzed as repeated cross-sectional estimates with person weights and 80 replicate weights. BLS LAUS supplies 2019–2024 statewide rates and counts for 50 states and D.C. These are descriptive sources, not a causal design.

**Join.** HPS is aggregated before an approximate state/collection-period match to BLS: 459 state-cycle rows, no unmatched keys. BLS measures the state's labor market, not the work status of each HPS respondent. Cycle overlaps weight unadjusted monthly counts before deriving the context rate. The separate monthly timeline uses adjusted rates; annual comparisons use published unadjusted averages.

**Definitions.** Hardship means somewhat/very difficult usual expenses; frequent loneliness means always/usually lonely; frequent anxiety symptoms means more than half the days/nearly every day in the previous two weeks. These are self-reports, not diagnoses. Income is 2023 household income; not working in seven days is broader than BLS unemployment. Ages are approximate broad groups.

**Missingness and comparability.** Income is invalid/missing for 14.35–18.52% and expenses for 5.37–11.24% of records, depending on cycle. Missingness may be nonrandom; the marginal files cannot establish its mechanism. Census documents prepaid-wireless contact-frame expansion at Cycle 8 and warns about comparability. Its contribution to the observed missingness drop is unquantified. Cross-cycle changes are not service-demand changes.

**Uncertainty and groups.** We show marginal 90% HPS intervals and valid n/Kish effective n/missing n. The project suppresses estimates below valid n=100 or effective n=30. This does not guarantee unbiased or precise estimates. State/national and pairwise ranking claims need more than interval overlap. Virginia's Cycle 9 worked/under-$50k hardship estimate remains suppressed at valid n=98. Counts of adults are point estimates, not clients or service capacity; count intervals require replicate totals.

**Time scope.** The core contains no pre-2024 direct loneliness baseline. Earlier expense-difficulty observations exist outside this selected core and are not pooled. Only the labor-market series supports the 2019–2024 recovery comparison. We do not follow the same people over time.

**Descriptive association.** State rank correlations are weak positive point associations, around 0.10–0.21 across cycles. The plotted state-resampling range is descriptive, not a survey-design interval or proof of no relationship. Unemployment alone has not been validated as a need-targeting measure.

**Unmet requests.** The state exports do not provide county/service-area or client operating data. Optional income-conditioned social-outcome analysis needs new respondent-level intersections. See [request dispositions](round1_request_status.csv) and [methods](../docs/ROUND1_METHODS.md).
