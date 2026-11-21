# Dashboard Requirements Document
**Economic Hardship and Social Well-Being During Pandemic Recovery**  
*Phase 2, Step 3 | Revised November 21, 2026*

This document follows the assignment's six required categories. It reflects the recorded Maya and Jordan stakeholder conversations, the AI-simulated Dr. Elena Chen skeptical review, and the team's analysis of Census Household Pulse Survey (HPS) and BLS Local Area Unemployment Statistics (LAUS). The expert role-play is not an independent statistical audit. Supporting evidence and transcripts are maintained separately in the project repository.

## 1. The Real Need

Our Phase 1 questions focused on whether improvements in unemployment coincided with lower household financial hardship and better social well-being. Stakeholder discussions showed that one broad recovery narrative would not answer the decisions our audiences actually face. **Maya Rodriguez**, a workforce-policy analyst, needs to compare labor-market conditions against 2019 without confusing lower unemployment with a complete recovery. **Jordan Lee**, a nonprofit program manager, needs to understand reported expense difficulty, the number of adults potentially affected, and which groups warrant further investigation; he cannot select service locations from statewide survey estimates.

The dashboard's purpose is therefore to **help users explore labor-market conditions, household expense hardship, and associated social outcomes as distinct but related indicators**, with visible uncertainty and clearly defined units. It should help users ask: Where was the 2024 unemployment rate at or below 2019, and did employment and labor-force counts move in the same direction? Where was hardship common, including among adults who worked recently? How did loneliness and anxiety symptoms differ across hardship and age groups? Which comparisons are too unstable or incomplete to support a conclusion?

The output is a **descriptive planning and exploration tool**, not a causal model, clinical diagnostic instrument, official measure of program eligibility, or county-level staffing/allocation system. An observed association cannot establish that unemployment or COVID-19 caused hardship or mental-health symptoms.

## 2. Audience

**Maya Rodriguez — policy decision-maker, Virginia Department of Labor and Industry.** Maya understands workforce statistics and can act on program priorities or policy reviews. She needs a quick state comparison of unemployment rates, employment and labor-force changes, and unusually weak or conflicting recovery indicators. She expects clearly distinguished annual and monthly measures, an explicit at-or-below-2019 rule, and reliability warnings before interpreting hardship estimates. A rate-only "recovered" label or unsupported significance ranking would make the visualization misleading for her.

**Jordan Lee — end user, Community Bridge Network.** Jordan plans nonprofit outreach, financial assistance, benefits navigation, and referrals. He understands service delivery but needs clear survey definitions, usable filters, hardship percentages **and** estimated affected-adult counts, plus work/income and social-outcome comparisons. He would reject a dashboard that equates "did not work during the last seven days" with official unemployment or uses a state estimate as a list of clients. For actual staffing or site decisions, he additionally needs unduplicated requests and unmet need by ZIP/county, wait times, access barriers, and partner capacity; those data are outside this project.

**Dr. Elena Chen — skeptical domain expert and methodological reviewer.** Elena evaluates whether estimates and visual claims are defensible. Her review calls for explicit denominators, weights, confidence intervals, missingness, suppression, temporal alignment, and non-causal language. She is a quality-control stakeholder rather than the default public dashboard user.

**Secondary audience:** analysts, classmates, and informed public readers should be able to read every chart without knowing raw survey variable names. Definitions, sources, collection windows, and limitations must be accessible where conclusions appear.

## 3. Main Representations

**Data foundation and limits.** The analysis uses **610,755 HPS adult response records from 2024 Cycles 1–9** (January–September), with person weights and 80 replicate weights reported in the notebook, and **2019–2024 BLS LAUS state-level series** for the 50 states and Washington, D.C. HPS is a repeated cross-sectional survey, not a panel following individuals. Aggregating HPS by state and cycle and approximately time-aligning LAUS state context produces **459 joined state-cycle records with no unmatched keys**; this is **not** an individual-level match or exact calendar-month alignment. HPS estimates are weighted adult percentages among valid outcome responses, with reported **marginal 90% confidence intervals**. The project suppresses cells with **valid n below 100 or Kish effective n below 30**, a screening convention rather than a guarantee of precision or freedom from bias.

**A. Labor-market benchmark comparison (Q1).** A sortable state table and a connected-dot/dumbbell view should display **2019, 2020, and 2024 published annual unemployment rates**, the **2020 seasonally adjusted monthly peak**, and changes in annual employment and labor-force counts and percentages from 2019 to 2024. Published annual rates are unadjusted; the adjusted monthly peaks must be labeled separately. Under the strict rule, **21 of 51 jurisdictions had a published 2024 annual unemployment rate at or below 2019**. Exact published ties count. The separate **±0.1 percentage-point display band** is not statistical equivalence and does not change the strict rule. For example, Virginia changed from **2.8% to 2.9%** and therefore fails the strict at-or-below test even though employment and labor force increased. As Maya and Elena emphasized, an improved rate alone is **not proof of complete recovery**.

**B. State expense-hardship overview (Q2 and the service-planning need).** The landing view should show the percentage reporting that paying usual household expenses was **"somewhat" or "very" difficult**, by state and HPS cycle, alongside a national reference and a companion estimate of the **number of adults reporting hardship**. Include valid respondent n, Kish effective n, missingness, marginal 90% interval, and reliability status. Adult counts are **weighted population point estimates**, not households, clients, applications, waitlists, or observed service demand; no count confidence interval is available in the current aggregate exports. The state-level Spearman correlations between unemployment and hardship are only approximately **+0.10 to +0.21** across cycles. Jurisdiction-resampling ranges are descriptive sensitivity checks, **not** HPS survey-design confidence intervals or proof that there is no relationship. Retain a secondary unemployment–hardship scatterplot to explain why the unemployment rate has **not been validated as a standalone hardship proxy**, not to rank funding need.

**C. Work and 2023 household income (Q3).** A six-category grouped chart or heatmap should compare hardship for those who **worked for pay or profit during the preceding seven days** and those who did not, within 2023 household-income groups **under $50,000**, **$50,000–$99,999**, and **$100,000 or more**. The national Cycle 9 hardship point estimate for recent workers in the under-$50,000 household-income group is approximately **55.78%**. This is not a claim that work caused or prevented hardship; "did not work" is not official unemployment. A requested Virginia Cycle 9 estimate for that same subgroup is **suppressed at hardship valid n = 98 and effective n ≈ 49.23**, because it fails the valid-n threshold. Suppression means no reliable displayed estimate under the project rule, **not zero hardship or zero need**.

**D. Loneliness and anxiety by hardship (Q4).** Paired comparison charts should show reported **frequent loneliness** ("always" or "usually") and **frequent anxiety symptoms** ("more than half the days" or "nearly every day") for adults with versus without reported expense hardship. In Cycle 9, rounded national point estimates are **21.0% versus 8.2%** for loneliness and **26.9% versus 9.7%** for anxiety; the analogous Virginia estimates are **25.7% versus 6.4%**, and **33.8% versus 7.4%**. These are self-reported survey outcomes, not clinical diagnoses. Display marginal 90% intervals and outcome-specific sample counts; **do not claim statistically significant contrasts** without covariance-aware tests, which the existing exports do not provide. Jordan considers this view relevant to voluntary referral planning; Elena requires that it not imply causation or proven effectiveness of a referral intervention.

**E. Age and social support (Q5).** A secondary national comparison should show frequent loneliness and lack of social support across approximate age groups **18–34, 35–64, and 65+**, with optional state views only when reliable enough to display. National point patterns may not hold within an individual state. Suppressed state-age cells must remain identified as suppressed rather than omitted silently or represented as zero.

**Cross-cutting comparability warning.** Census documented a **Phase 4.2 contact-frame expansion to prepaid wireless numbers beginning in Cycle 8**. Expense-item missingness fell from about **10.63% in Cycle 7 to 5.37% in Cycle 8**; the frame change's contribution to that difference is **unknown**. Every relevant cycle chart must mark the boundary and state: **"Documented Phase 4.2 contact-frame change; effects on estimates uncertain."** HPS cycle changes are not trajectories of the same people and should not be interpreted as changes in actual service demand.

These representations reflect the challenge round: rate-only "recovery" became an explicit multi-indicator benchmark; the unemployment–hardship relationship was demoted from a potential explanatory centerpiece to a cautionary descriptive comparison; and survey reliability and non-causal language became visible requirements, not just footnotes.

## 4. Exploration Tasks

Users must be able to:

1. **Choose a location and time.** Select any state (Virginia by default), the national reference where applicable, and any of HPS Cycles 1–9. Show the actual collection dates.
2. **Evaluate labor-market benchmarks.** Sort/filter the 51-jurisdiction recovery table by 2019/2024 rates, strict at-or-below flag, 2020 annual rate/adjusted monthly peak, and employment or labor-force change. Find cases where rates improved while counts fell; explain exact ties and the independent ±0.1-point display band.
3. **Explore scale versus prevalence.** Switch between hardship percentages and estimated affected-adult point counts; compare a selected state's estimates against a national reference without claiming a statistically significant difference.
4. **Explore subgroup patterns.** Compare the six recent-work × 2023-household-income groups, then switch between loneliness and anxiety by hardship group; permit age-group comparisons only with the appropriate state/national reliability context.
5. **Inspect reliability before interpretation.** Reveal valid n, effective n, outcome-specific missing n or missingness, 90% marginal interval, suppression status, definition, source and units for each displayed estimate. Suppressed values must never appear as zero.
6. **Recognize measurement changes.** Mark Cycle 8 clearly in cycle trends, explain the documented frame change, and distinguish HPS survey outcomes from LAUS contextual indicators and their approximate temporal match.
7. **Understand boundaries.** Clearly communicate that state rankings are descriptive, counts do not measure client demand, anxiety questions are not diagnoses, and neither source supports individual-level causal claims.

These tasks reflect requests repeated by Maya and Jordan: selectable state and cycle, usable comparisons, understandable definitions, counts alongside rates, and visible uncertainty.

## 5. Conflicts

**Opening emphasis — labor market or hardship?** Maya favors a recovery-led policy perspective; Jordan favors hardship-first service context. **Decision:** open with state hardship and affected-adult estimates, with a prominent **Labor-Market Benchmarks** section accessible directly. Historical recovery leads with employment and labor-force changes beside annual unemployment; a separate current-conditions view may lead with a current seasonally adjusted unemployment rate. Do **not** combine the indicators into a composite "need" score.

**State estimates versus local action.** Jordan wants county/ZIP demand and service-capacity measures before choosing staff or sites. **Decision:** first release remains descriptive at the state level. An explicit note says these data cannot identify local clients or determine service locations; those decisions require additional operational data.

**Simple rankings versus uncertainty.** Maya finds point-estimate ordering useful for triage, while Jordan needs credible broad comparisons and Elena objects to unsupported significance hierarchies. **Decision:** allow sorting with visible intervals, sample information and suppression; do **not** attach ordinal significance ranks, pairwise statistical-tie labels, or resource-allocation categories.

**Visible trends versus changing survey methods.** Users want cycle-to-cycle comparisons, but Cycle 8 introduced a documented frame change and altered missingness. **Decision:** retain the plots with a prominent boundary/qualification, never a seamless, causally interpreted recovery trajectory.

**Detail versus readability.** Elena demands methodological transparency; Maya and Jordan need decision-oriented displays. **Decision:** concise chart-level definitions and warnings first, with an expandable methods panel for variance estimation, missingness, reliability, and join details.

## 6. Must-Have vs. Nice-to-Have Charts and Features

**Must-have charts and views**

- **State hardship overview:** weighted percentage by state and cycle, national reference, marginal 90% intervals, sample/reliability information; companion affected-adult **point-count** view.
- **State profile:** default Virginia; clearly separate work/income hardship, loneliness/anxiety by hardship, age/social-support context, and suppressed cells.
- **Labor-market benchmarks:** sortable 51-jurisdiction comparison and connected-dot/dumbbell chart with annual rates, 2020 adjusted monthly peak, employment/labor-force changes, strict rule and display band.
- **Work × income and social-outcome comparisons:** six work/income groups and paired loneliness/anxiety comparisons with definitions, intervals and suppression.
- **Reliability and comparability:** state-by-subgroup suppression/reliability view where needed; explicit Cycle 8 annotation in cycle series; secondary descriptive unemployment–hardship scatterplot.

**Must-have functionality and acceptance checks**

- State selector, cycle selector, national reference, sortable/filterable recovery table, percentage/estimated-count toggle, and readable labels/legends.
- Each HPS estimate identifies the outcome, group, cycle, **percent units**, valid n, effective n, marginal 90% interval, missingness and source. Each LAUS measure identifies whether it is a rate, count, annual unadjusted measure or monthly adjusted measure.
- Suppressed estimates remain marked **"suppressed"**, never zero. The Virginia Cycle 9 recent-worker/under-$50k hardship cell must be suppressed at **valid n = 98**.
- Tooltips or a methods panel explain weighting, limits of marginal intervals, the descriptive state-level join, comparison restrictions, and the documented Phase 4.2 change.
- No causal, clinical, significance-ranked, exact-time-matched, or county-specific staffing claims appear without additional appropriate evidence.

**Nice-to-have, after the core is readable and accurate**

- Small-multiple state unemployment timelines; a state map that does not suggest county precision; downloadable filtered data; and a user-controlled display of strict versus ±0.1-point benchmark categories.
- County/metro indicators **only with a suitable new geographic source**, nonprofit operating records (inquiries, unmet demand, waitlists, access barriers and referrals), and further respondent-level intersections or properly designed covariance-aware comparison tests if new analysis supports them.

**Outstanding team verification (not represented as completed):** The notebook documents 20/20 **automated** raw-to-processed spot checks. The assignment separately calls for team **manual inspection of at least 20** cases; that private review and any discrepancies must still be recorded. Independent verification of replicate-weight variance formulas and formal contrast tests were not completed by the simulated expert role-play. The dashboard is a future implementation; this document defines its requirements.

**Project records:** [Updated datasheet](../personas/datasheet_summary.md) · [Round 2 stakeholder synthesis](../personas/round2_completion.md) · [Elena full simulated conversation](../personas/Persona3/conversation.txt) · [Challenge log](../personas/round3_challenge_log.md) · [Notebook](../notebooks/COVID_Recovery_Step0.ipynb)
