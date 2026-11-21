# Step 3: Dashboard Requirements Document

> **Revised Phase 2 requirements — 2026-11-21.** Incorporates the recorded [Round 2 Maya/Jordan replies](../personas/round2_completion.md), a transparently **AI-simulated** [Dr. Elena Chen Round 3 critique](../personas/round3_elena_review.md), and the [challenge log](../personas/round3_challenge_log.md). The simulated expert is not a real independent statistical audit or an additional HOKIEAI transcript. The source notebook still requires the team's **manual** 20-case raw-to-processed check. These pending verifications are not represented as completed.
>
> The final design choices below are **team-proposed requirements based on these reviews**. They do not amount to a built dashboard, a causal analysis, a significance-ranked state comparison, or eligibility/staffing recommendations.

## Economic Hardship and Social Well-Being During Pandemic Recovery

### 1. The Real Need

The dashboard will help two groups make better decisions:

- **State policy makers and workforce agencies** need to evaluate labor-market recovery.
- **Community-service organizations** need to understand where financial hardship remains high and how many adults may be affected.

The original Phase 1 plan focused mainly on whether lower unemployment was associated with lower hardship. Maya's Round 2 emphasis on genuine labor-market context and Jordan's Round 2 emphasis on household needs changed the focus; the simulated Elena Round 3 review further restricted what the claims may infer. The dashboard should now help users answer four practical questions:

1. Has a state’s labor market recovered compared with 2019?
2. Where is financial hardship still common, and how many adults does it affect?
3. Which work and income groups experience the greatest hardship?
4. Is financial hardship associated with loneliness and anxiety?

The dashboard must also show how reliable each estimate is. Users should see sample size, confidence intervals, missingness, and suppression flags instead of seeing numbers without context.

The dashboard will **not** use unemployment alone to rank need, prove causal relationships, diagnose mental-health conditions, or estimate actual service demand. It must not imply that the same HPS adults were followed over time, that state LAUS rates are respondents' unemployment statuses, or that approximate cycle-to-month alignment is exact. It will show descriptive patterns that can support further investigation and planning.

### 2. Audience

#### A. State policy makers and workforce agencies

These users understand unemployment rates, employment counts, labor-force counts, and policy indicators. They need to:

- Compare 2019, 2020, and 2024 unemployment rates by state.
- See the 2020 monthly peak as well as the 2020 annual average.
- Identify states that returned to or fell below their 2019 unemployment rate.
- See employment and labor-force changes alongside unemployment changes.
- Identify states where unemployment fell while the labor force also shrank.
- Understand when differences are too small or uncertain to support a strong ranking.

#### B. Community-service organizations and service planners

These users understand community needs and service delivery but may not know survey methodology in detail. They need to:

- See the percentage of adults experiencing hardship.
- See the estimated number of adults affected.
- Compare hardship by work status and household income.
- Compare loneliness and anxiety between hardship groups.
- Examine a selected state, with Virginia as the default example.
- See sample sizes, confidence intervals, missingness, and suppression labels.

The estimated number of affected adults is a weighted population estimate. It is not a count of clients, service requests, or people currently waiting for help.

#### C. Analysts and informed members of the public

These users need clear definitions, source information, readable controls, and enough methodological detail to distinguish survey estimates from labor-market estimates.

### 3. Data and Scope

The dashboard combines two main sources:

- **Census Household Pulse Survey (HPS):** hardship, work, income, loneliness, anxiety, social support, age, and state identifiers.
- **BLS Local Area Unemployment Statistics (LAUS):** state unemployment, employment, unemployment counts, and labor-force counts from 2019–2024.

The prepared data contain:

- HPS summaries for Cycles 1–9.
- 459 state-cycle rows in the HPS–LAUS join.
- No unmatched records in the prepared join.
- Survey-weighted estimates with 90% confidence intervals where available.
- Valid respondent counts, Kish effective sample sizes and suppression flags for reliability checks. Display is suppressed where **valid n < 100** or **effective n < 30**; passing this project convention does not prove unbiasedness or sufficient precision. Virginia Cycle 9 recent worker/under-$50k hardship: **valid n=98**, **effective n≈49.23**, suppressed by the valid-n rule. The number 98 was mislabeled “effective n” in Maya's unmodified Round 2 conversation; this analyst correction does not change the conclusion.

Important limitations:

- HPS is an online, self-reported survey and may have nonresponse and coverage bias.
- HPS and LAUS measure different concepts. Their join is at the state and time-period level, not the individual level.
- HPS cycles do not correspond exactly to calendar months.
- Census documents a **Phase 4.2 contact-frame expansion to prepaid wireless numbers beginning in Cycle 8**. The effect of that change on estimates or the observed missingness decline is **not quantified or established**; cycle movements must not be presented as changes in service demand.
- The results describe associations and changes. They do not prove that unemployment or COVID-19 caused hardship, loneliness, or anxiety.
- The current data support state-level analysis, not reliable county- or service-area targeting.
- Service requests, waitlists, referral capacity, and language-access data are outside the current scope.

### 4. Main Representations and Claims

#### A. Labor-market recovery

Use a sortable state table and a connected-dot or dumbbell chart. Show:

- 2019 annual unemployment rate.
- 2020 annual unemployment rate.
- 2020 monthly peak.
- 2024 annual unemployment rate.
- Employment change.
- Labor-force change.
- Recovery category.

Primary **published unemployment-rate benchmark** rule (not proof that a state's employment, household welfare, or labor market fully recovered):

- **At or below 2019:** 2024 rate minus 2019 rate is less than or equal to 0.
- **Near-tie display band:** an independent, purely descriptive band for rate changes within ±0.1 percentage points. It overlaps the exact at/below flag for exact ties and small negative changes, and **does not redefine** the strict threshold.
- **Above 2019 under the strict rule:** any positive published difference, including +0.1 percentage points; show the separate display band when applicable.

The dashboard must explain that the annual rates are **published unadjusted averages**, whereas 2020 monthly peaks are from a **seasonally adjusted monthly series**, and that the rates are published to one decimal place. Arkansas and New Hampshire are exact ties under the primary rule. Virginia changes from 2.8% to 2.9%, so it does not meet the strict rule but belongs in the near-tie category.

#### B. Financial hardship as the main organizing measure

The landing view should begin with hardship rather than unemployment. **This resolves a real Round 2 conflict:** Jordan wants immediate expense-hardship and affected-adult context, while Maya wants labor-market recovery foregrounded for policy analysis. The team chooses hardship first to support the cross-audience household-well-being task, with a prominent **labor-market recovery** tab/section and employment/labor-force change as its lead historical metrics. These are **not merged into a single need score**.

Show hardship by state and HPS cycle, compared with the national estimate. Include:

- Percentage of adults experiencing hardship.
- 90% confidence interval.
- Effective sample size.
- Reliability or suppression flag.
- Estimated number of affected adults.

A companion chart should show estimated adults affected in millions. The label must state that this is a weighted population estimate, not a client count.

#### C. Work and income differences

Show hardship for six work-and-income groups using a grouped bar chart or heatmap. Suppressed estimates must be labeled **suppressed**; they must never be changed to zero or silently removed.

The main claim is that working **for pay/profit in the past seven days** does not eliminate reported household expense difficulty. This is not official BLS employment/unemployment status and the income groups are from **2023 household income**, not current individual earnings. Working adults with lower household income can still report substantial difficulty paying expenses.

#### D. Hardship and social well-being

Use paired charts to compare frequent loneliness and frequent anxiety between adults with and without financial hardship.

For Cycle 9, the national results are approximately:

- Frequent loneliness: 21.0% among adults reporting hardship versus 8.2% among those reporting little or no hardship.
- Frequent anxiety: 26.9% versus 9.7%.

For Virginia, the corresponding results are approximately:

- Loneliness: 25.7% versus 6.4%.
- Anxiety: 33.8% versus 7.4%.

These rounded point estimates must be accompanied by their own valid-response sample counts and **marginal 90% confidence intervals** and a clear note: they are descriptive associations, not causal effects or clinical diagnoses. The current exports **do not provide covariance-aware confidence intervals/tests for differences between groups**, so the interface must not declare those contrasts statistically significant based on marginal interval overlap or separation.

#### E. Age and social support

Include an age-group view for loneliness and lack of social support. Separate national results from state results, and label suppressed or unreliable groups clearly.

This is a secondary view because stakeholders considered hardship, work, income, and social well-being more important than age-by-state comparisons.

### 5. Exploration Tasks and Interactions

The dashboard must allow users to:

1. Select a state. The default state should be Virginia, and users should also be able to select the national estimate.
2. Select an HPS cycle.
3. Compare a state with the national estimate.
4. Sort and filter the recovery table by unemployment rate, recovery category, 2020 peak, employment change, or labor-force change.
5. Read the recovery rule, including the treatment of ties and rounding.
6. Filter for states where unemployment fell but the labor force also fell.
7. Switch between hardship percentages and estimated adults affected.
8. Explore work status and income groups.
9. Switch between loneliness and anxiety.
10. See effective n, confidence intervals, missingness, and suppression status for each selected estimate.
11. Compare age groups at the national and state levels.
12. Read a short definition and source note for every major chart.
13. See a vertical Cycle 8 marker labeled: **“Documented Phase 4.2 contact-frame change; effects on estimates uncertain.”** It must not suggest that the frame change itself is unconfirmed.

### 6. Conflicts

#### Hardship-first versus recovery-first

Maya, the policy persona, preferred beginning with labor-market recovery and prioritizing **employment and labor-force changes since 2019** for a recovery view. Jordan, the community-service persona, preferred beginning with hardship and affected-adult context. The team opts for a **hardship-first public landing page** because it answers the cross-audience household-well-being purpose, while placing a prominent **recovery/context** section one navigation step away. Current seasonally adjusted unemployment should lead a *different* near-term labor-market conditions view. This explicit split avoids using an unemployment rate as a surrogate need score.

#### State-level versus local geography

Jordan requested county- or service-area information, but the current public HPS data do not support a reliable local dashboard. The first version will remain state-level and will clearly state that state estimates should not be used to choose specific neighborhoods or service locations.

#### Rankings versus uncertainty

Maya supports **point-estimate ordering for triage**, not inferential rank. Jordan supports ordering for funder/partner context, not client targeting. The sortable table will include valid n, effective n, marginal 90% intervals, missingness, reliability flags and the published-rate rule. There will be **no numbered significance ranks, formal high/low significance tiers, or pairwise statistical tie labels** without appropriate covariance-aware tests. Interval overlap by itself is not such a test.

#### Trends versus data-quality warnings

Both personas wanted cycle trends, but both noticed the Cycle 8 missingness change. The dashboard will preserve the trend while marking Cycle 8 on every relevant chart. It will not interpret that change as increased or decreased demand unless additional documentation confirms the cause.


### 7. Must-Have Charts and Features

#### Must-have charts

1. **Hardship overview:** hardship percentage by state and cycle, with national comparison, 90% intervals, effective n, and reliability status.
2. **Estimated adults affected:** weighted population estimates, preferably shown in millions.
3. **State profile:** hardship trend, work-by-income groups, hardship-group loneliness and anxiety, and age groups.
4. **Recovery table and chart:** 2019 rate, 2020 annual rate, 2020 monthly peak, 2024 rate, recovery category, employment change, and labor-force change.
5. **Work × income chart:** six groups, sample sizes, and suppression labels.
6. **Loneliness and anxiety chart:** comparison by hardship group, with intervals and non-causal wording.
7. **Reliability heatmap:** state-by-group view showing suppressed or low-sample estimates.
8. **Cycle 8 annotation:** visible on all cycle-trend charts, with the documented frame change and uncertain effect made explicit.

#### Must-have features

- State selector with Virginia as the default.
- HPS cycle selector.
- National-versus-state comparison.
- Sortable and filterable recovery table.
- Percentage/count toggle.
- Tooltips with definitions, sample size, intervals, and sources.
- Suppression handling that never converts suppressed values to zero.
- Missingness and reliability notes on every major view.
- Source and methodology panel.
- Readable colors, labels, and responsive layout.

### 8. Nice-to-Have Features

- Small multiples showing the unemployment timeline for all states.
- A state map, as long as it does not imply county-level precision.
- Downloadable filtered data.
- A toggle between the strict recovery rule and the ±0.1 percentage-point near-tie rule.
- County or metropolitan-area indicators **only after sourcing fit-for-purpose geographically representative and privacy-appropriate data**; the current HPS extracts do not support general county/client-service-area targeting.
- Community Bridge operational data, including service requests, waitlists, referral capacity, and language access.
- Further respondent-level analysis of hardship and social well-being by income, if the raw data support valid intervals.


### 9. Round 3 expert challenge outcome and claim policy

The transparent [Dr. Elena Chen role-play](../personas/round3_elena_review.md) tested all five findings. Its challenges **did not** independently certify the notebook but imposed stricter requirements on the dashboard narrative:

| Claim | Permitted interpretation | Prohibited overclaim |
|---|---|---|
| Q1 — labor-market | States' published 2019 vs 2024 LAUS rate benchmark, alongside employment/labor-force changes and 2020 monthly peaks | “State fully recovered” from a rate alone; treating adjusted monthly and unadjusted annual series as the same statistic |
| Q2 — HPS/LAUS relationship | Weak **equal-jurisdiction descriptive** correlations in the selected cycles; unemployment rate not validated as a hardship proxy | Proof of no association, formal survey-designed inference from state-resampling bands, ecological inference or causation |
| Q3 — work/income hardship | Weighted valid-answer hardship percentages conditional on seven-day recent work and **2023 household income** | Claim of unemployment status, precise current income/eligibility, or Virginia estimate where valid n=98 is suppressed |
| Q4 — loneliness/anxiety | Weighted self-reported symptom and loneliness point rates by hardship category, with each marginal 90% interval | Clinical diagnosis, causal relationship, or formal significant difference without replicate-based contrasts |
| Q5 — age/social outcomes | National age-by-cycle patterns and state comparisons **only where displayed reliability is adequate** | All states follow national pattern, suppressed groups have no need, or untested rank contrasts |

Specific correction from expert review: the existing Cycle 8 wording “possible survey change; cause unconfirmed” was misleading: **the contact-frame change itself is documented**, while its effect on estimates/missingness is unknown. Pairwise statistical comparison, replicate count-total confidence intervals, missingness sensitivity, and independent replication of the 80-replicate variance calculation are not claimed completed.

### 10. Required verification, acceptance criteria, and outstanding work

**Before Phase 2 evidence is signed off:** have a team member manually inspect **at least 20** original-vs-processed rows from the private case comparison, against the original source codes, log reviewer/date/findings and any remediation; the documented 20/20 automated check **does not count as human verification**. If the group needs independent confidence-interval method certification, separately inspect replicate-weight code and official design factors; the present Round 3 role-play is not that certification.

**Dashboard acceptance criteria once implemented:**
1. Every HPS chart carries exact outcome/cycle/population, percentage units, marginal **90% interval**, outcome-specific valid n/effective n, missingness/reliability access, and a readable definition.
2. Suppressed cells show “suppressed,” never zero; specifically Virginia Cycle 9 worker/under-$50k hardship is suppressed at **valid n=98**, despite effective n≈49.23.
3. Recovery keeps strict published-rate at/below distinct from ±0.1-point display bands, and keeps annual unadjusted data distinct from adjusted monthly peaks.
4. State-context HPS/LAUS comparisons disclose **approximate time matching** and do not imply personal or daily matching.
5. **Documented Phase 4.2** frame change appears on relevant cycle series; no uninterrupted trend is asserted across that boundary.
6. Adults-affected counts are clearly identified as weighted **point estimates**, not households, clients, unmet service demand, or error-bounded counts.
7. No causal, diagnostic, significance-ranked, or county-specific service-allocation conclusion appears without additional valid analysis/data.
8. Maya's recovery-oriented use and Jordan's hardship-first service context remain independently accessible without combining outcomes into a single score.

**Recorded status:** Maya and Jordan Round 2 responses are archived; the Elena challenge is a **labeled AI simulation** with an evidence-based disposition log. No new real-source respondent audit, independent variance-code verification, or built dashboard is claimed. These are explicit boundaries, not silent omissions.
