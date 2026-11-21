# Round 3 expert challenge log — Step 2 closeout

**Review date:** 2026-11-21. Sources: [Elena simulated transcript](round3_elena_review.md), [evidence packet](round3_evidence_packet.md), [original methods](../docs/ROUND1_METHODS.md). **Review type: transparent LLM persona simulation.** A comment by the simulated expert is **not independent verification** of calculations, or a claim that any unpublished code was run during this review.

| ID | Finding / method | Simulated skeptical challenge | Response and evidence | Decision | Dashboard/analysis consequence |
|---|---|---|---|---|---|
| C01 | F1 LAUS state recovery | Rate-at/below-2019 does not mean overall recovery; adjusted peak differs from unadjusted annual | Published M13 annual vs adjusted monthly 2020 peak; employment and labor-force changes in recovery table | **Reword** | State “2019/2024 unemployment-rate benchmark”, not absolute recovery; show count changes |
| C02 | F1 precision | ±0.1 pp category could be misread as statistical tie | Integer tenths compare published rates; band is display-only | **Clarified** | Exact published-rate rule separate from descriptive near-tie |
| C03 | F2 correlation | State resampling is not HPS survey-design inference | Methods say jurisdictions resampled and errors omitted; descriptive point correlations approx +0.10 to +0.21 | **Narrow claim** | Weak *descriptive* association, not proof of no relationship or a statistically valid ranking |
| C04 | F2 joining | HPS cycles cross months; LAUS only contextual | Aggregation at state×cycle; date-overlap-weighted unadjusted monthly LAUS counts; midpoint sensitivity | **Clarified** | Show approximate alignment and source-specific time/units; no individual match |
| C05 | F3 work/income | Recent work is not unemployment; 2023 income lagged | HPS definitions, outcome-specific valid respondents | **Retain with caveats** | Clear labels, income year, no eligibility/causal interpretation |
| C06 | F3 Virginia suppression | Maya miscalled n=98 effective size | Export: valid n=98; Kish effective n≈49.23; project rule valid n≥100 and effective n≥30 | **Correct factual annotation** | Suppress Virginia 2024 Cycle 9 worked/under-$50k hardship; do not display as zero |
| C07 | F4 mental health | Anxiety symptoms ≠ diagnoses; marginal estimates ≠ tested group difference | HPS coding and marginal 90% intervals, no covariance-aware contrast | **Retain descriptive point comparisons** | No cause/diagnosis/significance claim; add outcome-specific uncertainty |
| C08 | Cycle 8 | Frame expansion known, but effect on missingness unknown | Census Phase 4.2 user notes and cycle missingness logs | **Correct warning wording** | “Documented Phase 4.2 contact-frame change; effect on estimates uncertain” |
| C09 | HPS uncertainty | Were replicate scaling and contrasts independently audited? | Original notebook reports 80 replicates; no independent line-by-line formula audit in this review | **Open check** | Do not claim independent variance certification or pairwise confidence; audit before stronger inference |
| C10 | State comparisons | Marginal intervals alone don't show rank or difference | State/national overlap and missing covariance; methods already explicitly avoid tests | **Retain descriptive ordering** | Sortable point estimates with CIs but no significance tier or rank |
| C11 | Adult counts | Weighted point counts cannot be service demand; intervals unavailable | No replicate totals in exported count tables; local operational sources absent | **Retain context-only** | Label counts as adults (weighted point estimate), not households/clients; no count error bars |
| C12 | F5 age | National age patterns might not generalize to suppressed state cells | State-age valid/effective n and suppression exports | **Retain national descriptive views** | Suppressed state cells shown as unavailable for reliable comparison |
| C13 | Cleaning verification | Automated checks ≠ student human check of raw/processed rows | 20/20 automated, 180 fields passed; private human review explicitly pending | **Open required step** | Team must inspect at least 20 original/processed rows and sign off |
| C14 | Missingness | Mechanism unknown; excluding invalid responses may bias outcome estimates | Income missing 14.35–18.52%; expense missing 5.37–11.24%; no identified missingness mechanism | **Open limitation** | Missing n, sensitivity caveats, and no confident cross-cycle demand change |
| C15 | Decision scope | HPS state estimates cannot prescribe county staffing or referrals for actual clients | Jordan requests unmet local demand/service capacity; data not included | **Out of scope** | No geographic staffing/allocation prescription |

## Open items requiring team work (not marked complete)

- **Human Step 0 spot-check**: inspect the private original-versus-processed 20-case table against actual raw files; note reviewer/date, any mismatches, and remediation. Source files and private case table are intentionally absent from the public repository. The existing 20/20 result is automated only.
- **Independent survey-variance review**: inspect actual notebook code and Census replicate-weight documentation for scaling and 90% intervals; do not imply this was independently audited just because outputs exist.
- **Inferential contrasts** (optional for descriptive Phase 2; required before claims of significant pairwise/group/state differences): replicate-based covariance-aware comparisons; account for state within national.
- **Missingness sensitivity** (optional further analysis): evaluate how patterns change under reasonable exclusions/available-case variations; cannot infer missingness mechanism from marginal data.
- **Count uncertainty** (optional): replicate estimates of weighted adult totals if intervals are needed; do not scale percentage intervals.
- **New external data** (out of scope): county/ZIP client requests, unserved cases and service capacity for staffing decisions.

## Outcome

The simulated challenge round supports a **conditional descriptive dashboard**, not a causal or clinical conclusion. All five findings can appear with the revised definitions and reliability warnings; the F2 inferential interpretation and suppressed state subgroup claims are **limited or withheld**. No novel numerical conclusion has been inferred from the persona alone. The requirements draft can now be revised, but the student's human check and any instructor-specific transcript requirement remain separate responsibilities.
