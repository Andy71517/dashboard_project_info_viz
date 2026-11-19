# Round 1 review and completed follow-up analysis

Updated November 19, 2026. The repository was reviewed at commit `98e70bf`, including the recorded [Maya response](Persona1/response.md), [Jordan response](Persona2/response.md), and the partially implemented charts. The [original review](round1_review_original.txt) is retained unchanged for traceability. The original conversations and transcript PDFs have not been rewritten.

**Round 1 is closed with a disposition for every request.** This means the supported follow-up work has been implemented and limitations have been recorded; it does not mean every request is fully answerable. Round 2 persona replies remain to be recorded. The existing folder named `persona_round2` contains preparation evidence, not evidence that the next conversation happened.

## What the personas asked us to change

Maya prioritizes labor-market recovery, state comparisons, Virginia, and uncertainty. Jordan prioritizes hardship, the estimated number of adults reporting it, reliable within-state groups, and service relevance. Both want clear missingness and comparability warnings. Their preferences conflict on the opening view, percentages versus counts, and state-level context versus local operational decisions. These conflicts remain discussion topics; we have not invented a consensus.

## Corrections to the first review

- The observed state correlations are weak descriptive associations. A band obtained by resampling the 51 jurisdictions is **not** a survey-design confidence interval or proof of a null relationship. It omits HPS sampling error, LAUS model uncertainty and cross-cycle dependence. It cannot validate unemployment as a need proxy.
- A state's interval crossing the U.S. point estimate does not establish that the state and nation are statistically indistinguishable. The national sample includes that state. Those significance-like categories have been removed; the national figure is now only a descriptive reference.
- Percentage intervals must not be multiplied by an estimated population denominator to create count intervals. The covariance and replicate population totals are needed. Affected-adult counts are explicitly point estimates, not clients or capacity requirements.
- The exact Q1 rule remains published 2024 rate ≤ published 2019 rate. A separate ±0.1-point band flags small differences; it does not redefine recovery. Integer tenths remove floating-point boundary errors. Virginia is 2.8% → 2.9%: not at/below, but inside the ±0.1 display band.
- Census documents a contact-frame expansion to prepaid wireless numbers in Phase 4.2, beginning at Cycle 8. It warns that response rates and composition may affect comparability. This does not establish why our missingness declined. See [the documentation evidence](../docs/ROUND1_METHODS.md).
- The selected HPS core has no pre-2024 loneliness series. Earlier expense-difficulty data do exist, but they are not pooled into this 2024 analysis. We no longer suggest that no earlier hardship measurement exists.

## Request-by-request disposition

The machine-readable version is [round1_request_status.csv](round1_request_status.csv). The same table appears with saved output in the [notebook](../notebooks/COVID_Recovery_Step0.ipynb).

| ID | Request | Requested by | Status | Reason and boundary |
|---|---|---|---|---|
| 1 | Sortable annual-rate table | Maya | answered | 51-state sortable HTML and CSV include 2019, 2020 and 2024 annual rates. |
| 2 | Exact recovery, ties and rounding | Maya | answered | Integer tenths implement exact <=0; a separate +/-0.1 display band handles rounding without redefining recovery. |
| 3 | 2020 monthly peaks | Maya | answered | Seasonally adjusted monthly peaks and all tied months are recorded separately from annual averages. |
| 4 | Employment/labor-force changes and decline flags | Maya | answered | Counts, percentage changes and separate flags for both employment and labor-force declines are exported. |
| 5 | State-by-cycle hardship and reliability | Both | answered | 459 rows include 90% intervals, valid n, Kish effective n, missingness and explicit project-rule flags. |
| 6 | Descriptive association, not need targeting | Maya | answered | Captions and methods distinguish a point association and state-resampling sensitivity from survey inference or a targeting rule. |
| 7 | Virginia work/income and social outcomes | Maya | partially answered | Intervals and valid n are shown. The Cycle 9 worked/under-$50k hardship cell remains suppressed (valid n=98); no pooling or imputation. |
| 8 | Uncertainty and ties in rankings | Maya | partially answered | Marginal intervals and rounded display ties are supplied; they do not establish pairwise differences or statistical ties. Covariance/replicate contrasts are needed. |
| 9 | Explain the Cycle 8 missingness change | Both | partially answered | Census confirms prepaid-wireless frame expansion and comparability warning. Its causal contribution to the observed missingness decline cannot be identified here. |
| 10 | Hardship percentage and affected adults | Jordan | answered | Point counts and valid-population denominators accompany percentages. Count intervals are not available from marginal percentage CIs; counts are not clients. |
| 11 | Reliable state work/income breakouts | Jordan | partially answered | All states/cycles and a suppression map are available; unreliable cells remain hidden rather than filled in. |
| 12 | Missing-data note on relevant views | Jordan | answered | Chart captions, state profile and all-cycle evidence tables identify valid-answer denominators and missingness. |
| 13 | Avoid reading cycle changes as demand changes | Jordan | answered | Cycle 8 frame-change markers and comparability warnings appear on the cycle-trend views; Phase 4.2 is not joined into a clean recovery trend. |
| 14 | Reliable age subgroups, national vs state | Both | answered | Both loneliness and support have 90% intervals and suppression flags; separate national/state estimates and an all-state age reliability map are provided. |
| 15 | Q4 conditioned on income | Analyst suggestion, not a persona request | out of scope | Optional additional hypothesis. Current marginal aggregates do not identify this intersection; new respondent-level cross-tabs/variance work would be required. |
| 16 | County or service-area indicators | Jordan | not answerable with this data | Selected exports support states, not counties or client service areas. Metro identifiers in some raw files do not provide county coverage. |
| 17 | Requests, waitlists, referral capacity and language access | Jordan | out of scope | These operational measures require Community Bridge data; HPS/LAUS do not measure them. |

## What was completed

The notebook retains the original preparation and the student's added Charts 7–16, fixes their inference/caption issues, and now executes the follow-up views too. It includes Virginia intervals, explicit suppression, outcome-specific sample sizes, a correct recovery table with count changes and peak-month ties, all-state/all-cycle hardship evidence, work/income and age reliability maps, and documented Cycle 8 markers. The sortable table and seven follow-up figures are in the [Round 1 evidence pack](../reports/round1_followup/state_profile_focus.html). Download that HTML and open it in a browser to use the sort controls.

The [completion record](round1_completion.md) lists the verification and what still needs data or judgment. Use the [Round 2 handoff](round2_handoff.md) for the next real role-play conversation. No Round 2 persona responses or Round 3 skeptical-expert review have been generated.
