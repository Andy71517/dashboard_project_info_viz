## Datasheet summary (for Round 1)

**Data.** Two sources, used descriptively (not causally):
- **Census Household Pulse Survey (HPS), Jan–Sep 2024, Cycles 1–9:** 610,755 adult responses on expense difficulty, work, income, loneliness, support and anxiety. Each cycle is a new cross-section, weighted to adults, with 90% intervals.
- **BLS LAUS, 2019–2024:** state unemployment rate and employment, unemployment and labor-force counts for 50 states and D.C.

**Join.** HPS is summarized by state and cycle, then matched to LAUS on state and approximate collection months: 459 state-cycle rows, none unmatched.

**Definitions.** Hardship = expense paying "somewhat" or "very" difficult. Frequent loneliness = "always" or "usually". Frequent anxiety = nearly every day or more than half the days (not a diagnosis). Income is 2023 household income. "Did not work" is not the same as unemployed.

**Limitations**
1. **Survey self-reports.** Low response and nonresponse bias remain. Income is missing for 14–19% of respondents and the expense question for 5–11%, and missing answers are not random. Missingness drops sharply at cycle 8, and the cause is undocumented.
2. **State-level match only.** LAUS describes the state, not the respondents. The state link is weak (rank correlation 0.10–0.21, band includes zero in every cycle) and cannot show cause.
3. **No pre-2024 baseline for hardship or loneliness.** "Recovery" is labor-market only.
4. **Small groups.** Smallest state sample is 347 valid answers, and some state-by-age estimates are suppressed.
5. **Coarse variables.** Income is lagged, age is approximate, and overlapping groups cannot be summed.
