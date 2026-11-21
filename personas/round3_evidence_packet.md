# Round 3 evidence packet — Dr. Elena Chen

**Prepared:** 2026-11-21. **Scope:** recorded project analysis plus the completed Maya/Jordan Round 2 discussions. This packet contains **analyst-presented claims**, not an independent audit or a completed third-party expert judgment. The accompanying Elena review is explicitly a **simulated persona role-play**.

## Provenance and scope

- Census Household Pulse Survey (HPS), Cycles 1–9 in 2024: **610,755 raw response records**, weighted survey estimates; 80 replicate weights are reported as used by the notebook. HPS is a series of cross-sectional samples, **not longitudinal tracking**.
- BLS Local Area Unemployment Statistics (LAUS), 2019–2024: state annual and monthly labor-market indicators for 50 states and D.C.; adjusted 2020 monthly peaks are **not** the same measure as unadjusted annual averages.
- HPS state × collection cycle joined to approximately time-aligned BLS context: **459 state-cycle rows, zero unmatched** in the exported join. Joined records are **not matched people**.
- Definitions: hardship = **somewhat/very difficult to pay usual household expenses**; recent work = worked for pay/profit in last seven days; income = **2023 household income before tax**; frequent loneliness = **always/usually**; frequent anxiety symptoms = **more than half the days/nearly every day** (not a clinical diagnosis); age groups = approximate **18–34, 35–64, 65+**.
- Percentages use outcome-specific valid-response denominators and person weights; reported 90% marginal confidence intervals, valid sample n, Kish effective n and missing n accompany estimates. **Rule for display:** suppress if valid n <100 or effective n <30. This is a project stability screen, *not* an official validity test.
- Census documents that Cycle 8/Phase 4.2 expanded the contact frame to prepaid wireless numbers. This raises comparability concerns but **does not establish the cause or magnitude** of observed missingness changes.

Primary supporting files: [datasheet](datasheet_summary.md), [methods](../docs/ROUND1_METHODS.md), [validation](../docs/ROUND1_VALIDATION.md), [cleaning log](../audit/step0/cleaning_decisions.csv), [source provenance](../audit/step0/input_provenance.csv), [execution notebook](../notebooks/COVID_Recovery_Step0.ipynb), [figures and captions](../reports/round1_followup/), [Round 2 synthesis](round2_completion.md).

## Findings and questions for critical scrutiny

### F1 — State labor-market recovery is multidimensional

The [51-jurisdiction recovery export](../reports/round1_followup/state_recovery_table_with_flags.csv) identifies **21** jurisdictions with published **2024 annual unemployment rate ≤ published 2019 annual rate**. Exact ties count; a separate **±0.1 percentage-point display band** is a rounding aid, **not equivalence or recovery certification**. Arkansas and New Hampshire are published exact ties. Virginia goes **2.8% (2019) → 2.9% (2024)**; it does **not** satisfy strict at/below, though it is in the separate near-tie display band. The Virginia peak in April 2020 is **11.9% adjusted monthly**. Virginia employment and labor-force annual counts rose relative to 2019. Louisiana and Maryland illustrate states with lower published annual unemployment rates but **lower** employment and labor-force counts.

**Challenge requested:** Do these different LAUS series support the label “recovery”? Are exact-rate ties, time baselines, adjustment methods and percentage/count changes sufficiently differentiated? Should we limit the claim to “comparison with a 2019 benchmark”?

### F2 — The state-level unemployment/hardship relationship is weak *as described*, and should not be used as a validated hardship proxy

The project reports cycle-specific jurisdiction-level descriptive Spearman correlations **about +0.10 to +0.21** (Cycle 9 primary-alignment point statistic **0.0956** in [run_summary.json](../audit/step0/run_summary.json)). A midpoint alignment sensitivity for Cycle 9 yields **0.1298**. The reported resampling ranges include zero, but the resampling treats 51 jurisdictions as exchangeable, **not** the HPS complex sample design. These ranges omit uncertainty in HPS percentages, BLS estimation and repeated cycles. They cannot prove a zero population association.

**Challenge requested:** Does the descriptive evidence support “unemployment is insufficient to predict hardship,” or only the narrower “the plotted simple state-level relationship is weak”? How should BLS/HPS temporal alignment and alternative population weighting affect interpretation? Avoid ecological inference.

### F3 — Financial hardship is reported among adults who worked recently

National work/income chart and [all-cycle national estimates](../reports/round1_followup/national_group_estimates_and_samples.csv) show hardship among **worked in last seven days / under $50k 2023 household income**: **55.78% in Cycle 9** (point estimate; the exported marginal 90% CI is available). This is a conditional survey estimate—not the fraction of all workers who need aid, a causal effect of having a job, or an eligibility screen. At Virginia Cycle 9, the corresponding work/low-income **hardship valid n is 98**, **Kish effective n ≈49.23**, so the hardship point estimate is **suppressed under the project n≥100 rule**. The term “98 effective n” appearing in Maya's Round 2 answer was a mislabeling.

**Challenge requested:** Are person-level work/income constructs, household denominators, lagged income, coverage, nonresponse and subgroup sizes described sufficiently? Does national evidence justify anything about suppressed Virginia cells?

### F4 — Hardship and frequent self-reported loneliness/anxiety symptoms co-occur

The [working requirements draft](../reports/step3_requirement.md) summarizes Cycle 9 **national** frequent loneliness **21.0% vs 8.2%**, frequent anxiety **26.9% vs 9.7%**, among the hardship and little/no-difficulty groups, respectively. The draft summarizes **Virginia** loneliness **25.7% vs 6.4%**, anxiety **33.8% vs 7.4%**, respectively. These are **rounded, reported descriptive point estimates** from existing draft/aggregate evidence; retain chart intervals, outcome-specific valid n and exact collection cycle in any publication. No formal contrast variance is shown for the *difference* between the groups. Neither illness diagnosis nor direction of causality is established.

**Challenge requested:** Could wording imply causal mental-health effects, clinical prevalence, individual-level progression or proven significant differences? Are missing responses and uncertainty treated correctly?

### F5 — National age differences are visible; small within-state age groups may not sustain the same claims

The 2024 HPS national cycle-by-age charts show different point rates of frequent loneliness and lack of support across the approximate 18–34, 35–64 and 65+ age groups. Several state-age cells are suppressed, including relevant Virginia Cycle 9 cases. Avoid broad “every state follows the national pattern” claims; display outcome-specific validity flags and do not equate suppression with absence of need.

**Challenge requested:** Are age construction, missingness, multiple comparisons, precision, and nationally versus locally generalizable claims sufficiently clear?

## Specific methodological matters to interrogate

1. **Variance/weights:** confirm the exact 80-replicate algorithm, scale, 90% multiplier and appropriateness for subgroup estimates; do not assume the public statement “80 replicate weights” settles correctness.
2. **Denominators:** are all reported percentages on outcome-eligible valid HPS respondents, not total observations/households? Are the weighted adult counts point-only?
3. **Missingness:** income missingness **14.35–18.52%** across cycles; expense-item missingness **5.37–11.24%**. Test sensitivity if possible; the mechanism of missingness **has not been identified**.
4. **Cycle 8:** distinguish documented survey-frame expansion from unexplained missingness changes, and do not infer real service-demand shifts.
5. **LAUS time alignment:** date-overlap-weighted unadjusted *counts* generate context rates for HPS cycles; midpoint sensitivity is available. Avoid asserting an exact monthly/daily/individual match.
6. **Ranking:** marginal 90% intervals, even when they overlap or not, do not by themselves establish paired-state tests or national comparisons with shared respondents.
7. **Populations and units:** weighted adult people vs households vs service clients; percentage points vs rates vs headcounts; current work vs official unemployment.
8. **Reproducibility:** cleaned aggregate and joins are validated by automation, including 20/20 machine spot-check cases and 180 field comparisons. **The separate human inspection of those 20 raw/processed cases is still pending**; do not describe it as done.
9. **Operational action:** no county/client ZIP demand, waiting lists, referrals, or organizational capacity is in the selected sources. Neither stakeholder may claim these exist.

## Round 3 interview questions

For each F1–F5: **(a)** Is the descriptive finding supportable on supplied evidence? **(b)** What is the strongest counterargument or measurement concern? **(c)** What exact test/documentation would settle it? **(d)** What wording and dashboard design would you permit? **(e)** Which questions are unanswerable with current exports?

Ask the expert to explicitly say **“I don't know”** where source evidence is insufficient. Record challenges in [round3_challenge_log.md](round3_challenge_log.md), using **verified, corrected, conditional, or unresolved** rather than an imaginary expert signoff.
