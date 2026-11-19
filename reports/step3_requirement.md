# Step 3: Dashboard Requirements Document
## Economic Hardship and Social Well-Being During Pandemic Recovery

### 1. The Real Need

The dashboard will help two groups make better decisions:

- **State policy makers and workforce agencies** need to evaluate labor-market recovery.
- **Community-service organizations** need to understand where financial hardship remains high and how many adults may be affected.

The original Phase 1 plan focused mainly on whether lower unemployment was associated with lower hardship. Stakeholder feedback changed the focus. The dashboard should now help users answer four practical questions:

1. Has a state’s labor market recovered compared with 2019?
2. Where is financial hardship still common, and how many adults does it affect?
3. Which work and income groups experience the greatest hardship?
4. Is financial hardship associated with loneliness and anxiety?

The dashboard must also show how reliable each estimate is. Users should see sample size, confidence intervals, missingness, and suppression flags instead of seeing numbers without context.

The dashboard will **not** use unemployment alone to rank need, prove causal relationships, diagnose mental-health conditions, or estimate actual service demand. It will show descriptive patterns that can support further investigation and planning.

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
- Effective sample sizes and suppression flags for reliability checks.

Important limitations:

- HPS is an online, self-reported survey and may have nonresponse and coverage bias.
- HPS and LAUS measure different concepts. Their join is at the state and time-period level, not the individual level.
- HPS cycles do not correspond exactly to calendar months.
- Cycle 8 has a noticeable change in missingness. The cause is not confirmed, so it must not be presented as a real change in demand.
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

Primary recovery rule:

- **At or below 2019:** 2024 rate minus 2019 rate is less than or equal to 0.
- **Near tie:** the difference is within ±0.1 percentage points.
- **Above 2019:** the difference is greater than 0.1 percentage points.

The dashboard must explain that the rates are published to one decimal place. Arkansas and New Hampshire are exact ties under the primary rule. Virginia changes from 2.8% to 2.9%, so it does not meet the strict rule but belongs in the near-tie category.

#### B. Financial hardship as the main organizing measure

The landing view should begin with hardship rather than unemployment. This reflects the community-service use case and the stakeholder feedback.

Show hardship by state and HPS cycle, compared with the national estimate. Include:

- Percentage of adults experiencing hardship.
- 90% confidence interval.
- Effective sample size.
- Reliability or suppression flag.
- Estimated number of affected adults.

A companion chart should show estimated adults affected in millions. The label must state that this is a weighted population estimate, not a client count.

#### C. Work and income differences

Show hardship for six work-and-income groups using a grouped bar chart or heatmap. Suppressed estimates must be labeled **suppressed**; they must never be changed to zero or silently removed.

The main claim is that having a job does not eliminate financial hardship. Working adults with lower household income can still report substantial difficulty paying expenses.

#### D. Hardship and social well-being

Use paired charts to compare frequent loneliness and frequent anxiety between adults with and without financial hardship.

For Cycle 9, the national results are approximately:

- Frequent loneliness: 21.0% among adults reporting hardship versus 8.2% among those reporting little or no hardship.
- Frequent anxiety: 26.9% versus 9.7%.

For Virginia, the corresponding results are approximately:

- Loneliness: 25.7% versus 6.4%.
- Anxiety: 33.8% versus 7.4%.

These numbers must include confidence intervals and a clear note: they are descriptive associations, not causal effects or clinical diagnoses.

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
13. See a vertical Cycle 8 marker labeled: **“Possible survey change; cause unconfirmed.”**

### 6. Conflicts

#### Hardship-first versus unemployment-first

Maya, the policy persona, preferred beginning with labor-market recovery. Jordan, the community-service persona, preferred beginning with hardship. The dashboard will open with hardship because it is closer to service-planning decisions. A prominent labor-market recovery section will remain available for policy users.

#### State-level versus local geography

Jordan requested county- or service-area information, but the current public HPS data do not support a reliable local dashboard. The first version will remain state-level and will clearly state that state estimates should not be used to choose specific neighborhoods or service locations.

#### Rankings versus uncertainty

Maya requested state rankings. Rankings can make small differences look important, so the table will include confidence intervals, effective n, reliability flags, and the recovery-rule explanation. The dashboard will avoid presenting uncertain differences as definitive rankings.

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
8. **Cycle 8 annotation:** visible on all cycle-trend charts.

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
- County or metropolitan-area indicators after privacy and data-quality review.
- Community Bridge operational data, including service requests, waitlists, referral capacity, and language access.
- Further respondent-level analysis of hardship and social well-being by income, if the raw data support valid intervals.
