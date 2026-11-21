# Step 2, Round 3 — Dr. Elena Chen skeptical-expert role-play

**Date:** 2026-11-21. **Nature of record:** an **AI-simulated** skeptical-expert review produced from the exact Dr. Elena Chen persona prompt supplied by the team and [the shared evidence](round3_evidence_packet.md). This is **not** a separate HOKIEAI ONEchat session, independent peer review, real university expert consultation, or rerun of the raw HPS notebook. The analyst responses below represent evidence/documentation already inspected. Where exported data do not establish a statistical test or cleaning claim, that point remains unresolved rather than “approved.”

**Persona instruction:** Dr. Elena Chen, labor economist and survey-methods researcher at a university-affiliated public-data quality center; skeptical, precise and evidence-focused; challenge every substantive claim, do not defer to interviewers, do not invent data or statistics, say “I don't know” when information is absent. See [persona_prompts.md](persona_prompts.md).

**Analyst presents:** F1–F5 and source definitions/methods exactly as set out in [round3_evidence_packet.md](round3_evidence_packet.md), and the Round 2 context from [round2_completion.md](round2_completion.md).

---

## Challenge 1 — F1: “Recovered” by which measure?

**Dr. Chen:** “Your 21-jurisdiction figure uses 2024 *annual unadjusted unemployment rates* at or below the 2019 published rate. But a state with a lower rate may also have fewer employed people and a smaller labor force. Why are you calling that a recovery? Also, are your 2020 monthly peaks adjusted while annual rates are unadjusted? Those aren't interchangeable.”

**Analyst:** “Agreed. The 21 count is a clearly defined **rate-benchmark category**, not a declaration of comprehensive labor-market or household recovery. We use published unadjusted M13 annual averages for the 2019/2024 comparison and separately labeled 2020 seasonally adjusted monthly peaks. We show employment and labor-force changes concurrently. The [recovery table](../reports/round1_followup/state_recovery_table_with_flags.csv) records Louisiana and Maryland with lower published rates but falling employment/labor-force counts. We will rename the claim to **‘2019–2024 state labor-market benchmark comparison’**, and avoid an unqualified ‘recovered’ badge.”

**Dr. Chen:** “That's defensible descriptive wording. Use the exact published-rate rule and disclose measurement bases. Do not give your ±0.1 display band the status of a confidence interval or statistical tie.”

**Disposition:** **Revised wording; data-supported comparison.**

## Challenge 2 — F2: The correlation band is not a survey interval

**Dr. Chen:** “You say your Spearman correlations are about +0.10 to +0.21 and that resampling ranges cross zero. Were you resampling the HPS complex survey respondents with replicate weights, or treating the 51 jurisdictions as exchangeable observations? What does that band actually mean?”

**Analyst:** “The latter. Our [methods notes](../docs/ROUND1_METHODS.md) already say the state-resampling bands are only **descriptive sensitivity ranges**. They omit the survey sampling uncertainty in hardship estimates, modeled LAUS uncertainty, and cross-cycle dependence. We withdraw any language asserting that the population association has been proven absent or the relationship is ‘statistically insignificant.’ The more supportable point is that the **simple equal-jurisdiction descriptive association is weak in the plotted cycles**, and an unemployment rate has not been validated here as a hardship-targeting proxy.”

**Dr. Chen:** “I accept that narrower point. A proper design-aware analysis of the association would require survey-design uncertainty and a clearly stated inference target. Do not interpret an interval containing zero as proof of no relationship.”

**Disposition:** **Interpretation corrected; inferential strength unresolved.**

## Challenge 3 — F2: Does the join create a false impression of precision?

**Dr. Chen:** “How can a cross-sectional individual household survey be ‘matched’ to monthly state unemployment when HPS cycles cross calendar months? Do your joins follow individual respondents or exact days? Could a different month alignment change the correlations?”

**Analyst:** “HPS estimates are first aggregated to state × cycle; no person-to-person join exists. We attach state **context** by overlap-weighted unadjusted monthly LAUS counts, then derive a context rate. We also provide a midpoint-month alignment sensitivity table. Cycle 9's descriptive Spearman point value is **0.0956** under primary alignment and **0.1298** under midpoint alignment ([run_summary.json](../audit/step0/run_summary.json)). Both are positive and small; we do not generalize these two values to all cycles or claim the exact day is observed.”

**Dr. Chen:** “Then label the rate ‘approximately time-aligned LAUS state context.’ The sensitivity comparison is useful but does not establish exactness, causality, or universally negligible alignment uncertainty.”

**Disposition:** **Existing method validated as descriptive context; stronger claims ruled out.**

## Challenge 4 — F3: “Worked” isn't unemployment, and the income year matters

**Dr. Chen:** “Are you treating adults who didn't work for pay during the last seven days as unemployed? Is the $50,000 threshold current individual earnings?”

**Analyst:** “No. The project uses ANYWORK, a seven-day recent-work self-report, not BLS unemployment status. Income represents **2023 household income before tax** and may not capture the respondent's current economic situation. The observed Cycle 9 national point estimate **55.78%** for hardship among recent workers from under-$50k households is a conditional survey estimate and does not establish who is eligible for services or the effect of employment.”

**Dr. Chen:** “That descriptive finding may be shown if the denominator, survey weight, cycle, interval and missingness are attached. Do not call it a measure of ‘working poor unemployment,’ and don't convert it into an eligibility rule.”

**Disposition:** **Conditional finding retained with definitional qualification.**

## Challenge 5 — F3: The suppressed Virginia cell has been described incorrectly

**Dr. Chen:** “Maya says the Virginia Cycle 9 recent-worker/under-$50k cell has an effective sample size of 98. But I want the *unweighted valid n* and Kish effective n separately. Which triggered suppression?”

**Analyst:** “The [Virginia aggregate export](../reports/round1_followup/focus_state_estimates.csv) has **hardship valid n = 98**, **Kish effective n ≈ 49.23**. The cell is suppressed because **valid n <100**; Kish effective n is above the separate 30 threshold. Maya conflated the quantities in her conversation. The exported estimate is suppressed, and we will not show or infer its hardship percentage from any hidden value.”

**Dr. Chen:** “Correct the transcript **in an analyst annotation**, not by silently rewriting the persona's historical words. State what was suppressed and why. The threshold is a screening convention, not a proof that n=100 is reliable and n=98 is not.”

**Disposition:** **Verified labeling correction; subgroup remains unanswerable at prescribed reliability rule.**

## Challenge 6 — F4: Are you claiming causation or clinical illness?

**Dr. Chen:** “Your national and Virginia loneliness and anxiety gaps are potentially important, but ‘hardship leads to anxiety’ would be unsupported. Does the anxiety question diagnose a disorder? Have you calculated the sampling variance of the *between-hardship-group differences*?”

**Analyst:** “No clinical diagnosis or causal direction is inferred. Frequent anxiety is coded as reported symptoms more than half the days or nearly every day in the prior two weeks; loneliness is always/usually. The exported figures give **marginal** weighted percentages and 90% CIs. The project has **not** provided covariance-aware confidence intervals for the *difference* between hardship groups. We therefore say ‘higher reported point estimates’ and give both separate intervals, without a formal significance claim about the difference.”

**Dr. Chen:** “That presentation is acceptable as a descriptive association if the source/cycle/valid n are visible. Remove any phrase like ‘the difference is statistically significant’ unless you do the correct survey-weighted contrast.”

**Disposition:** **Descriptive finding retained; difference-inference unresolved.**

## Challenge 7 — HPS missingness and the Cycle 8 break

**Dr. Chen:** “You've noticed a sharp reduction in expense-item missingness at Cycle 8. Are you claiming the contact-frame change caused it? And are you using Cycle 1–9 movements as a clean longitudinal recovery story?”

**Analyst:** “No. Census documents an expansion to prepaid wireless contacts with Phase 4.2. Our measured expense missingness fell from **10.63% in Cycle 7 to 5.37% in Cycle 8**, and income missingness from **18.09% to 14.35%**; we cannot attribute those falls to that change without new evidence. The HPS consists of repeated independent cross-sectional samples, not tracked people. Relevant figures identify Cycle 8 and prohibit interpreting the change as actual service demand.”

**Dr. Chen:** “Use **‘Documented Phase 4.2 contact-frame change; effects on estimates uncertain’** instead of ‘possible survey change; cause unconfirmed.’ That is more precise.”

**Disposition:** **Annotation correction required; actual missingness mechanism unresolved.**

## Challenge 8 — Confidence intervals and ranking validity

**Dr. Chen:** “Do your 90% intervals come from the correct 80 replicate weights and variance factors? Has an independent reviewer inspected the notebook's formula? And do overlapping state and U.S. intervals justify saying two places are statistically tied?”

**Analyst:** “The notebook and supporting documentation report the 80 replicate weights and marginal intervals. The committed aggregate tables carry valid n, effective n, SE and intervals, and automated notebook checks are recorded. We **have not independently verified every replicate-variance formula in this review**, and marginal intervals do not establish pairwise ties or significance, particularly where state and national estimates overlap in respondents. Our state list is sorted **descriptively**, never called an inferential rank. An independent formula/code audit and covariance-aware contrasts are follow-up work for stronger inference.”

**Dr. Chen:** “Then label statistical verification as pending wherever that specific audit was not done; don't imply that successful notebook execution independently validates every formula.”

**Disposition:** **Marginal intervals reported; independent variance audit and paired contrasts unresolved.**

## Challenge 9 — Population counts are not clients or service capacity

**Dr. Chen:** “When you estimate the number of adults in hardship in a state, are these actual observed people needing appointments, or a weighted projection? Where are the count confidence intervals? Could your dashboard justify a staffing decision from these numbers?”

**Analyst:** “They are weighted adult **population point estimates among valid responders**, not counts of clients, households or service requests. We don't derive count intervals by multiplying percentage intervals by a weighted denominator. Replicate-total analysis is necessary for those intervals. No county/ZIP unmet-need counts or organizational service operations are in the selected data. Jordan's staffing question cannot be answered by this project alone.”

**Dr. Chen:** “Retain count points with explicit caveats; reject facility locations, county targeting, staffing recommendations and funding allocations inferred from those estimates.”

**Disposition:** **Descriptive counts retained; operational decisions out of scope.**

## Challenge 10 — F5: Age patterns, suppression and generalizability

**Dr. Chen:** “A national pattern does not guarantee the same pattern for Virginia or any other state. How do you know which state-age contrasts are reliable? Are intervals comparisons of groups or separate margins?”

**Analyst:** “We have distinct national and state age estimates, outcome-specific valid/effective n, marginal CIs and suppression labels in the state-age exports. The approximate age bands are 18–34, 35–64, and 65+. The dashboard will not claim a universal state-level pattern, infer missing values as zero, or treat marginal interval overlap as a formal age contrast.”

**Dr. Chen:** “Then national age comparisons may be shown as secondary descriptive context. When state cells are suppressed, say the data don't support that state subgroup comparison, not that it has no need.”

**Disposition:** **Qualified national description retained; suppressed state claims withheld.**

## Challenge 11 — Code audit and manual spot-check are not identical

**Dr. Chen:** “You tell me the data were cleaned and checked. Who examined the original records? Does an automated 20/20 pass mean a human inspected the 20 rows and checked the cleaning log's rejected alternatives?”

**Analyst:** “No. The repository records 226 passing notebook checks and **20/20 automated raw-to-processed spot checks** with 180 field comparisons. [START_HERE.md](../docs/START_HERE.md) and [quality_checks.json](../audit/step0/quality_checks.json) explicitly say the independent **human review of the private 20-case table remains pending**. We cannot complete that portion without opening the uncommitted private comparison/raw files. The cleaning log documents 208 decisions, but a human signoff has not been supplied.”

**Dr. Chen:** “That's a real outstanding assignment requirement. Do not label the full data-cleaning review complete until the team signs off on at least 20 manually inspected cases and records exceptions, if any.”

**Disposition:** **Manual verification outstanding; not passed or fabricated.**

---

## Elena's conditional review conclusion

**Dr. Chen (simulated):** “I would not approve an unrestricted ‘pandemic recovery caused better well-being’ narrative. Your descriptive state labor-market comparisons, weighted hardship patterns, work/income group comparisons, and self-reported loneliness/anxiety contrasts are useful **when the observation units, time windows, missingness, weighting, suppression and limitations accompany them**. I accept the narrower statements, not causal inferences or confident subgroup rankings. The strongest unresolved matters are independent verification of the 80-replicate variance implementation, missing-data sensitivity, covariance-aware comparisons, and the project's pending human review of its 20 original/cleaned cases. HPS/LAUS alone cannot decide county-level staffing or actual service demand. The final dashboard should make those boundaries obvious to a non-expert.”

## Team response / next action

1. Carry the claim and language corrections into [Step 3 requirements](../reports/step3_requirement.md).
2. Add permanent notes about **valid n 98 versus effective n ≈49.23** and the **documented** Cycle 8 frame change.
3. Preserve original stakeholder transcripts without rewriting their statements.
4. Treat human 20-case review and independent variance audit as **pending checks**, not as finished analyses.
5. If the instructor requires a distinct ONEchat/HOKIEAI transcript rather than an LLM role-play performed here, repeat this evidence packet in that tool and save the actual reply. This file is transparently labeled a simulated expert persona.
