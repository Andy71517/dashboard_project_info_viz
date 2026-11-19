# Round 1 review: what the personas told us, how each follow-up rates, and chart changes

Both personas accepted the core findings and kept a few questions, but they redirected the project in places. I checked Virginia figures and data availability directly in the processed CSVs. I couldn't re-run anything this turn, so any number I haven't checked is marked "from chart".

## 1. What the responses tell us

| Question | Maya (state policy) | Jordan (community services) | Takeaway |
|---|---|---|---|
| Q1 Recovery | High priority | Context only | Maya's main question. Jordan wants it only as background for funders. |
| Q2 Unemployment vs hardship | Diagnostic, not a targeting rule | Don't prioritize | Both read the weak correlation (0.10–0.21, band includes zero) as the finding: **unemployment is not a proxy for need.** This null result is worth keeping. |
| Q3 Work × income | High | **Top** | Both stress that working low-income adults have high hardship. |
| Q4 Loneliness/anxiety by hardship | High | **Top** | Both read it as a case for pairing financial help with referrals, and both repeat the "not causal, not a diagnosis" warning. |
| Q5 Age × state | Secondary | Secondary | Both accept the national age pattern and defer state-specific conclusions until reliability is shown. |

**New questions they raised**
- **Virginia-specific results (Maya).** Her questions are state-specific, and our charts default to New York, California and Texas.
- **How many people are affected, not just what share (Jordan).** A high percentage in a small state and a moderate one in a large state mean different workloads.
- **Which states "recovered" under a stated rule (Maya).** She wants ties and rounding handled, and she wants states flagged where the rate fell but the labor force shrank.
- **What the cycle 8 break is (both).** Both spotted the missingness drop at cycle 8 and won't read cycle-to-cycle changes as demand changes.
- **Operational data and sub-state geography (Jordan).** She wants this for service planning.

**Where they pull apart**
- **Question order:** Maya leads with labor-market recovery, Jordan with household hardship. Jordan wants the dashboard built around hardship, not unemployment.
- **Unit:** percentages (Maya) versus counts of adults (Jordan).
- **Geography:** Maya works at state level, while Jordan says state is too coarse for outreach placement.
- **Decision type:** Maya needs a state ranking with a tie rule, and Jordan needs reach by service group.

**One lead worth checking.** The notebook's input files are named "Phase 4.1" for cycles 4–7 and "Phase 4.2" for cycles 8–9. The cycle 8 missingness drop may be a Census instrument or mode change, not a real shift. Check the Phase 4.2 documentation in [source_documentation/](docs/source_documentation) before Round 3, because Dr. Chen will ask.

## 2. Follow-up classification

| # | Request | Who | Rating | Reason |
|---|---|---|---|---|
| 1 | Sortable state table with 2019, 2020, 2024 annual rates | Maya | **Answerable** | [state_recovery_2019_2024.csv](data/processed/state_recovery_2019_2024.csv) has them. Chart 8 shows it visually, but there is no table yet. |
| 2 | Rule for "at or below", including ties and rounding | Maya | **Answerable** | The rule is change ≤ 0 on published one-decimal rates. Arkansas and New Hampshire are exact ties and count as recovered. Virginia is +0.1 (2.8 to 2.9), so it fails the rule within rounding. A "within ±0.1" category would be fairer. |
| 3 | 2020 monthly peak | Maya | **Answerable** | The monthly series is seasonally adjusted. Virginia peaks at 11.9% in April 2020, against a 6.5% annual average, so "peak" must be defined. Chart 2 only shows 3 states. |
| 4 | Percent and count changes in employment and labor force, flagging states where the rate fell but the labor force fell too | Maya | **Answerable** | The data has it, and chart 8 shows the percent changes. From the chart, Mississippi, West Virginia, Wyoming and Louisiana look like cases, but the flag isn't computed. |
| 5 | State-by-cycle hardship with 90% intervals, effective n and a reliability flag | Maya, Jordan | **Answerable** | The CIs, `effective_n` and `suppressed` flags are in the data. Chart 9 covers only cycle 9 and shows no n. |
| 6 | Treat the association as descriptive, with no "need" ranking from unemployment | Maya | **Answerable** | A design and caption choice. Chart 10 already works this way. |
| 7 | Virginia Q3 and Q4 with intervals | Maya | **Partly answerable** | Q4 is fine (cycle 9 loneliness 25.7% vs 6.4%, anxiety 33.8% vs 7.4%, with intervals). Q3 has 5 of 6 groups. "Worked / under $50k" is suppressed in cycle 9 (98 valid answers, minimum 100). Pooling cycles would need respondent-level data for valid intervals. |
| 8 | Tie rule and uncertainty for all state rankings | Maya | **Answerable** | Chart 9 groups states as above, below or indistinguishable from the national estimate. For pairwise comparisons, use SE-based overlap (`hardship_se_pp` is in the data). It's approximate, because replicate-level covariance isn't available. |
| 9 | Explain the cycle 8 missingness change | Maya, Jordan | **Not answerable from our data** | It needs Census Phase 4.2 documentation. It is answerable from outside sources, and the phase labels point to an instrument change. |
| 10 | Where hardship is high and how many adults that represents | Jordan | **Answerable** | `hardship_weighted_numerator` gives estimated adults. For example, Virginia cycle 9 is about 2.18M of 6.27M adults. Intervals on the counts can be scaled from the percentage intervals. They are population estimates, not client counts. |
| 11 | Hardship by income and work status within states, only where reliable | Jordan | **Partly answerable** | The data has all state groups. Some cells are suppressed, such as the Virginia cell above. There is no view yet showing which states and groups pass the threshold. |
| 12 | Missing-data note on every view | Jordan | **Answerable** | The missingness table is already built. It needs to go into captions or footers. |
| 13 | Don't read cycle shifts as demand changes | Jordan | **Answerable** | Mark cycle 8 on every cycle-trend chart. |
| 14 | Flag unreliable age subgroups and separate national from state | Jordan, Maya | **Answerable** | Chart 7 already marks suppressed groups. It needs a reliability overview across states. |
| 15 | Q4 by income, to see whether income drives the gap | Neither asked (see below) | **Not answerable yet** | It needs the raw respondent files. This is item 9, which was left out. |
| 16 | County or service-area indicators | Jordan | **Not answerable** | HPS public files give state level. The raw files appear to carry a metro-area field for the largest metros (`EST_MSA`, which the notebook treats as private). That would need a pipeline change and a privacy review. |
| 17 | Service requests, unmet need, waitlists, referral capacity, language access | Jordan | **Out of scope** | These are Community Bridge's own operational data, not HPS or LAUS. They should go in the datasheet as an acknowledged gap. |

Item 15 is my addition, not a persona request. Both personas read Q3 and Q4 as supporting referral decisions, and Dr. Chen's likely challenge is that income, not hardship, drives the loneliness and anxiety gap. Leaving it unbuilt is fine for Round 2, but note it as a known gap.

## 3. Chart changes that would help the personas

**Priority 1: needed for Round 2**
1. **State profile page (new chart):** one state, defaulting to Virginia (`FOCUS_STATE = "51"`), with panels for hardship across the cycles against the national estimate, the six work × income groups with a "suppressed" marker, hardship-group loneliness and anxiety, and age groups. This serves Maya's Virginia request and Jordan's within-state breakouts.
2. **Q1 table and chart 8 revision:** add a sortable table (rate in 2019, 2020 annual and 2020 monthly peak, rate in 2024, change, employment and labor-force % change). Add three categories (at or below, within ±0.1, above) and a flag for states whose rate fell while the labor force shrank. In the dumbbell, replace the annual 2020 marker with the monthly peak, or show both.
3. **Chart 9 additions:** show valid n, a reliability flag and the estimated number of adults. A companion bar (adults affected, in millions) would answer Jordan's "how many" question and sit next to the percentage chart.
4. **Cycle 8 marker:** add a vertical line labeled "possible survey change; cause unconfirmed" to the cycle-trend charts (10, 12, 14, 15, 16).

**Priority 2**
5. **Reliability heatmap (extend chart 13):** a state × group grid (work × income, age) showing which estimates are suppressed, so Jordan's "only where reliable" request is visible.
6. **Sample sizes on bars and lines:** add n to the national work/income and hardship charts (3, 4, 15, 16). Maya and Jordan both ask for it.
7. **Chart 2:** add Virginia to the timeline states, or switch to small multiples for all states.
8. **Chart 10:** add quadrant labels listing states with low unemployment and high hardship (Wyoming, Oklahoma and similar), to make the "unemployment is not need" point concrete.

**Demote or fold in:** chart 1 (raw sample sizes) and chart 6 (histogram) are now covered by charts 13 and 8. Keep them in an appendix.

Everything in Priorities 1 and 2 can be built from the current processed CSVs without any download. If you'd like me to implement them, switch to an agent that can edit files and I'll build the Priority 1 set first.