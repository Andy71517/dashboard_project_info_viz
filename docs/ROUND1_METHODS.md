# Methods checked while closing Round 1

## Cycle 8 comparability

The original Census **Phase 4.2 Household Pulse Survey User Notes**, September 12, 2024, page 1, state that the contact frame newly includes prepaid wireless numbers. Census warns that this may affect response rates and sample composition and therefore comparability with earlier cycles. Cycles 8 and 9 run July 23–August 19 and August 20–September 16, 2024.

Source: [official Census PDF](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-2_2024_Household_Pulse_Survey_User_Notes_09122024.pdf); [saved original](source_documentation/Phase4-2_2024_Household_Pulse_Survey_User_Notes_09122024.pdf). The relevant page was text-extracted and visually inspected during this review. The wording is paraphrased here; no effect size or cause of the observed missingness change is inferred.

Measured expense-item missingness declines from 10.63% in Cycle 7 to 5.37% in Cycle 8; income missingness declines from 18.09% to 14.35%. The coincidence with a documented frame change is a comparability concern, not an attribution. The Phase 4.1 notes separately describe a gender/sexual-orientation split-panel experiment affecting those two items. That is not evidence that the same experiment caused changes in expense or social-item missingness.

All relevant cycle charts now mark the boundary between Cycles 7 and 8. Narrative captions do not describe the shifts as changes in service demand. The same people are not linked into individual recovery trajectories.

## Rates, rounding and recovery

Annual LAUS values are published unadjusted M13 averages. Monthly 2020 peaks use seasonally adjusted M01–M12 rates and preserve all tied peak months. The two statistics are labeled separately. A 2020 annual rate is not the monthly peak.

Compare integer tenths of the published annual rates, then divide the difference by ten. The exact indicator is `change_tenths <= 0`. Exact ties therefore count as at/below. A distinct display band is below by more than 0.1 point, within ±0.1 point, or above by more than 0.1 point. It is a rounding aid, not a statistical equivalence interval.

The table gives original 2019/2024 employment and labor-force counts, signed count changes, percentage changes, and separate flags for a lower unemployment rate accompanied by a shrinking labor force or employment. Virginia's published annual rate rises from 2.8% to 2.9%; employment rises by 136,041 persons and labor force by 147,523. Its 2020 monthly adjusted peak is 11.9% in April; its unadjusted annual average is 6.5%.

## HPS reliability, ranks and counts

Each outcome excludes its own invalid/missing answers. Valid n, missing n, Kish effective n, confidence intervals and suppression flags accompany the estimates. We retain the existing project thresholds: valid n ≥100 and effective n ≥30. Passing is not a guarantee of precision, representativeness or freedom from nonresponse bias.

Virginia Cycle 9 worked/under-$50k hardship has only 98 valid answers and remains suppressed. Its place in the plot is labeled suppressed rather than shown as a zero-length bar. Five other work/income estimates are available. No pooling or replacement was done to manufacture the missing sixth estimate.

The ordered state figure shows point-estimate order, marginal 90% intervals and a national reference. It does not assign above/below/indistinguishable significance labels. State and national estimates share respondents; arbitrary pairwise differences also require covariance information unavailable in the exported marginal summaries. Rounded display ties are labeled as display ties only.

Weighted hardship numerators estimate adults reporting hardship among valid responses. They are not households, clients, outreach targets or a count of unmet service demand. The supplied aggregates do not include replicate count totals, so count uncertainty is not calculated by scaling percentage intervals. A new replicate-total analysis would be needed for count intervals.

## Correlation bands

The point correlations summarize all 50 states and D.C. with equal jurisdiction weight. The existing 90% state-resampling bands are retained only as descriptive sensitivity ranges under an exchangeable-jurisdiction resampling assumption. They are not HPS survey-design confidence intervals and cannot establish statistical absence of a relationship. HPS uncertainty, BLS uncertainty and cross-cycle dependence are not incorporated. Median quadrants are exploratory labels, not validated need categories.

## Scope boundaries

County/service-area estimates and Community Bridge operating measures are not available in the selected exports. Some original HPS files contain selected metro identifiers; those do not supply general county coverage or service-area indicators. Income-conditioned hardship/social-outcome intersections are an optional analyst suggestion, not a request from either recorded persona. They require new respondent-level intersections and replicate variance work; marginal views cannot be joined to create person-level relationships.
