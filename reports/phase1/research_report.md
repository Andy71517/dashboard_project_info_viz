# Recovery beyond the unemployment rate
## Data acquisition and preparation report

**Scope:** U.S. labor-market recovery in 2019–2024, connected to household financial hardship and adult social well-being in January–September 2024. **Audit date:** November 2, 2026. **Audience:** a team of 3–4 CS graduate students building a public interactive visualization.

## 1. Executive summary and recommendation

**Use two sources: Census Household Pulse Survey (HPS), 2024 Cycles 1–9, and BLS Local Area Unemployment Statistics (LAUS).** Use the complete comparable 2019–2024 LAUS history for the recovery narrative and align its 2024 state observations to the nine HPS collection periods for the joined analysis. Reserve CDC BRFSS for an optional separate annual mental-health extension. Do not add it to the core dashboard.

This recommendation follows actual downloads, file inspection, codebook checks, weighted aggregation, and an executed join. The nine HPS files contain **610,755 measured respondent records**. Their state aggregates join to LAUS in **459 state-cycle rows (51 jurisdictions × 9 cycles), with zero unmatched keys on either side**. The join is one-to-one after aggregation. Neither replicate weights nor duplicated observations from a join are used to meet the size requirement. See the supplied audit CSVs, validation JSON, and preparation code for the evidence.

Three constraints materially change the initial project idea:

1. HPS introduced direct social-support and loneliness items on **January 9, 2024**. Its public CSV columns are `SOCIAL1` and `SOCIAL2`; `SOC1` and `SOC2` are questionnaire identifiers. There is no HPS loneliness baseline in 2019–2023. [Census Phase 4.0 user notes](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-0_2024_Household_Pulse_Survey_User_Notes_03252026.pdf)
2. The cross-sectional HPS ended September 16, 2024. The October 2024 transition and 2025 HTOPS change sampling, recruitment, collection modes, incentives, frequency, and geographic reporting. Do not splice these into a continuous state-level recovery series. [Census transition methodology](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Source_and_Accuracy_October_2024_FINAL.pdf)
3. October 2025 LAUS observations are unavailable, and its 2025 annual averages cover 11 months. **2024 is the latest complete comparable annual endpoint**, although flagged 2025 data have been downloaded and preserved as an optional extension. [BLS annual-revision notice](https://www.bls.gov/lau/launews1.htm)

The project can ask whether labor-market recovery coincides with household security, and which groups still experience hardship, loneliness, and frequent anxiety. It cannot identify the causal effect of COVID-19, demonstrate individual recovery trajectories, or measure a pandemic-wide change in loneliness.

## 2. Topic and question ladder

| Level | Proposed framing |
|---|---|
| Topic | Social and economic conditions surrounding the COVID-19 disruption and subsequent recovery in the United States. |
| Broad question | Does recovery in conventional labor-market indicators correspond to financial security and social well-being? |
| Bounded question | Across states, how did labor markets change from 2019 to 2024, and how did 2024 financial hardship relate to loneliness and support? |
| Measurable questions | Q1–Q5 below, using official LAUS rates/counts and weighted HPS adult percentages. |
| Exploration path | United States → state → one demographic or hardship group, plus year → month for LAUS and year → collection cycle for HPS. |

Use “recovery” operationally: a state’s 2024 unemployment rate relative to its 2019 value, supported by employment and labor-force counts. This does not imply every resident or every aspect of life recovered. “Economically vulnerable” means a declared income category or reported expense difficulty, not a poverty classification.

## 3. Five measurable research questions

The exact question is followed by the four assignment notes: measurement, row unit, audience, and a plausible surprising result. These are research questions; only the explicitly labeled preliminary calculations in Section 8 are completed substantive results.

### Q1. How uneven was labor-market recovery across states?

**Exact question.** Between 2019 and 2024, which states had a 2024 annual unemployment rate at or below their 2019 rate, and how do their monthly 2020 unemployment peaks and subsequent employment/labor-force trajectories differ?

**What to measure.** LAUS `series_id`, `year`, `period`, `value`, `measure_code`, and `seasonal`. Measure 03 is unemployment rate, percent of the civilian labor force; 04 is unemployed persons; 05 is employed persons; 06 is civilian labor-force persons. Use published not-seasonally-adjusted `M13` annual observations for annual comparisons. Use seasonally adjusted `M01`–`M12` series for monthly recovery curves. Calculate the annual rate difference in percentage points. Never sum percentages or mix adjusted and unadjusted observations in one series.

**Unit of analysis.** One state × month × adjustment status after pivoting the four measures into columns; a separate annual table contains one state × year. Restrict to 50 states plus D.C. Annual recovery comparisons end in 2024; 2025 is an explicitly incomplete extension.

**Intended audience.** Students, workforce agencies, and local policy analysts who want to see where an apparently national recovery concealed different state trajectories.

**Surprising result.** A state could return to its old unemployment rate while employment and labor-force counts follow quite different paths. Lower unemployment alone may give an incomplete account of recovery.

### Q2. Does low unemployment coincide with low household hardship?

**Exact question.** In each 2024 HPS cycle, how strongly is state-level expense hardship associated with contemporaneous LAUS unemployment, and which states combine relatively low unemployment with relatively high hardship?

**What to measure.** HPS `EXPNS_DIF` (questionnaire `SPN4`), coded 1 not at all difficult, 2 a little, 3 somewhat, 4 very difficult, referring to paying usual household expenses in the last seven days. Define serious hardship as codes 3–4 among valid 1–4 responses and calculate an adult-weighted percentage with `PWEIGHT`. Join the resulting state-cycle percentage to the day-overlap-aligned LAUS unemployment rate and counts. Show a per-cycle scatterplot, descriptive Spearman rank association, and quadrant positions relative to the displayed state medians. The median split is a visualization aid, not an official poverty or recovery threshold.

**Unit of analysis.** One state × HPS collection cycle, 459 rows. The **required independent-source join** uses two-digit state FIPS and cycle, with a period-to-month bridge. HPS adults 18+ and LAUS labor-force participants 16+ are distinct populations; unemployment is contextual exposure, not a survey respondent attribute.

**Intended audience.** Community organizations, students, and policymakers testing whether favorable labor-market headlines capture the difficulty households report paying bills.

**Surprising result.** Several low-unemployment states may still report substantial hardship, or the state-level association may be weak despite a strong within-survey relationship between work status and hardship.

### Q3. How much hardship remains among adults who recently worked?

**Exact question.** Within each 2024 cycle, what is the hardship-percentage gap between adults who did and did not work for pay or profit in the previous seven days, separately within household-income bands under $50,000, $50,000–$99,999, and $100,000 or more?

**What to measure.** HPS `ANYWORK`: 1 yes, 2 no; valid `EXPNS_DIF` as in Q2; `INCOME` categories 1–8, grouped 1–3, 4–5, and 6–8. The 2024 questionnaires ask about **2023 total household income before tax**. Retain both work groups in each income band; report weighted hardship percentages and differences in percentage points. `ANYWORK=2` includes retired people, students, caregivers, and others: call this “did not work,” not “unemployed.” Income is categorical and lagged; do not calculate a mean income from its codes.

**Unit of analysis.** One geography × cycle × work-status/income combination, derived from respondent-level HPS records using `PWEIGHT`. Start nationally; allow state selection where estimates pass the project’s reliability rule. The supplied `work_income` groups implement these six combinations. A national estimate uses respondent weights directly, not the average of state percentages.

**Intended audience.** Student researchers and service organizations interested in financial difficulty among people who are working, and in how household resources modify the comparison.

**Surprising result.** Low-income adults who worked could still have high hardship, and some nonworking high-income adults could report relatively little hardship. Work status is not synonymous with economic security.

### Q4. How do loneliness and frequent anxiety differ by expense hardship?

**Exact question.** In each 2024 cycle, what are the percentage-point gaps in frequent loneliness and frequent anxiety between adults reporting somewhat/very difficult expenses and adults reporting not-at-all/a-little difficult expenses?

**What to measure.** HPS `SOCIAL2`: 1 always, 2 usually, 3 sometimes, 4 rarely, 5 never feeling lonely. Define frequent loneliness as 1–2 among valid 1–5. `ANXIOUS`: 1 not at all, 2 several days, 3 more than half the days, 4 nearly every day, over the preceding **two weeks** in the 2024 instrument. Define frequent anxiety as 3–4 among valid 1–4. Split by valid `EXPNS_DIF` groups. Use `PWEIGHT` and metric-specific valid denominators. The anxiety measure is one symptom-frequency item, not a clinical diagnosis, a GAD-2 score, or loneliness.

**Unit of analysis.** One geography × cycle × hardship group. Each outcome has its own denominator and confidence interval. The supplied preparation code computes both outcomes for these groups. Differences within a cycle can use replicate estimates of the difference; do not infer significance just from whether two marginal confidence intervals overlap.

**Intended audience.** Campus and community support planners interested in overlapping economic, social, and emotional needs, without equating those needs.

**Surprising result.** The hardship gap might be much larger for anxiety than for loneliness, or a visible association nationally might weaken in a particular state. That would challenge a single “distress” explanation.

### Q5. Does the national age pattern of social support hold within states?

**Exact question.** In each 2024 cycle, how do lack-of-support and frequent-loneliness percentages differ among adults aged approximately 18–34, 35–64, and 65+, and does the national ordering hold when drilling into a state?

**What to measure.** HPS `SOCIAL1`: 1 always, 2 usually, 3 sometimes, 4 rarely, 5 never obtaining needed social and emotional support. Define lack of support as 3–5, following the CDC HPS indicator definition. Use `SOCIAL2` frequent loneliness as in Q4. Approximate age as 2024 minus `TBIRTH_YEAR`, which is top/bottom coded; group it rather than treating it as exact age. `ABIRTH_YEAR` identifies imputed birth year. Use `EST_ST`, cycle, `PWEIGHT`, and all 80 person replicate weights.

**Unit of analysis.** One geography × cycle × age group. This question requires an interactive **United States → state → age group** drill-down. Group ordering is descriptive when uncertainty is large; hide unreliable point estimates and show a clear unavailable message.

**Intended audience.** Student affairs teams, community organizations, and researchers testing assumptions about older adults’ social isolation and younger adults’ support needs.

**Surprising result.** Younger adults might report more loneliness than older adults, or a state might reverse the national ordering. Support and loneliness need not rank groups identically.

## 4. What was actually acquired and inspected

### 4.1 Verification boundary

**Measured from files:** HPS respondent row counts, headers, selected-column types and codes for representative 2020–2023 releases and all nine 2024 cycles; the February 2025 HTOPS file; LAUS bulk observations and metadata; all records in 2019 and 2025 BRFSS ASCII files; missingness; replicate-key matches; the aggregate join; and selected comparisons against Census published tables.

**Verified from documentation only:** BRFSS 2020–2024 full-file row counts and geographic participation; variable availability in those annual codebooks; details of the HPS/HTOPS redesign. Those intervening BRFSS raw annual files were not downloaded. No claim is made to have harmonized or analyzed all years of BRFSS or every original HPS survey period.

**Proposed or still to complete:** the dashboard, all five complete research analyses, formal gap significance tests and multiple-comparison decisions, production reliability review, and a final hosted-site privacy review. The delivered data products are preparation/audit outputs, not a finished dashboard or causal study.

The attached screenshots were read as assignment evidence. Their illustrative examples were not treated as instructions to change the topic or collect unrelated transit data.

### 4.2 HPS: actual files and coverage

Each downloaded CSV archive includes a respondent file, a replicate-weight file, and an Excel dictionary. The raw unit is one responding adult reporting on themselves and aspects of their household. These are repeated cross-sections, not a person-level panel spanning the pandemic.

| Release actually opened | Collection interval | Measured respondent rows | CSV columns |
|---|---|---:|---:|
| 2020 Week 1 | Apr 23–May 5, 2020 | 74,413 | 82 |
| 2020 Week 13 | Aug 19–31, 2020 | 109,051 | 188 |
| 2021 Week 22 | Jan 6–18, 2021 | 68,348 | 204 |
| 2022 Week 41 | Dec 29, 2021–Jan 10, 2022 | 74,995 | 208 |
| 2023 Week 63 | Oct 18–30, 2023 | 79,371 | 247 |
| 2024 Cycle 1 | Jan 9–Feb 5 | 68,544 | 170 |
| 2024 Cycle 2 | Feb 6–Mar 4 | 71,152 | 170 |
| 2024 Cycle 3 | Mar 5–Apr 1 | 71,798 | 170 |
| 2024 Cycle 4 | Apr 2–29 | 73,352 | 181 |
| 2024 Cycle 5 | Apr 30–May 27 | 72,162 | 181 |
| 2024 Cycle 6 | May 28–Jun 24 | 72,125 | 181 |
| 2024 Cycle 7 | Jun 25–Jul 22 | 70,429 | 181 |
| 2024 Cycle 8 | Jul 23–Aug 19 | 59,913 | 220 |
| 2024 Cycle 9 | Aug 20–Sep 16 | 51,280 | 220 |
| February 2025 HTOPS, inspected then excluded | Feb 21–Mar 7, 2025 | 6,740 | 206 |

The 2020–2024 files above each contain 51 state jurisdictions. `EST_ST` is state FIPS; `EST_MSA` identifies selected large metros, not all counties or cities. `REGION` is available from Phase 2 in inspected files. No county join or comprehensive state → county drill-down is supported by these HPS files. Week numbers are collection labels, not seven-day intervals; 2024 cycles are four-week intervals. The raw files do not supply a respondent interview date suitable for a daily HPS chart: add release dates through a documented period lookup. [Census historical PUF index](https://www.census.gov/programs-surveys/household-pulse-survey/data/datasets.2024.html)

The raw Cycle 9 count is 51,280, matching the Census release page’s response count. CDC’s social-connection page reports a smaller analytic sample (50,813 for this period). These counts describe different processing/analytic populations. This report uses the **measured PUF count**, never substitutes an analytic or weighted count for raw rows. [Census Cycle 9 release](https://www.census.gov/data/tables/2024/demo/hhp/cycle09.html), [CDC analytic overview](https://www.cdc.gov/nchs/covid19/pulse/lack-socialconnection.htm)

### 4.3 HPS variable verification and introduction dates

| Questionnaire item / real CSV column | Meaning and codes | Verified availability and preparation decision |
|---|---|---|
| `SPN4` / `EXPNS_DIF` | Household expense difficulty during last 7 days; 1 not at all, 2 a little, 3 somewhat, 4 very. | Absent in Week 1; present in first Phase 2 file, Week 13, beginning Aug 19, 2020. In that early dictionary it is item 19a; later instruments use `SPN4`. Present in all nine 2024 files. Do not mistake later dictionary phase lists beginning at 3.2 for the first appearance of the underlying measure. |
| `SOC1` / `SOCIAL1` | Needed social/emotional support; 1 always, 2 usually, 3 sometimes, 4 rarely, 5 never. | Introduced Phase 4.0, Jan 9, 2024; present in all nine cycles. Not present under these names in inspected 2020–2023 releases. |
| `SOC2` / `SOCIAL2` | Feeling lonely; same 1–5 frequency codes. | Introduced Jan 9, 2024; all nine cycles. No earlier HPS loneliness measurement is inferred. |
| `EMP2` / `ANYWORK` | Any work for pay/profit in last 7 days: 1 yes, 2 no. | Present from inspected Week 1 (Apr 23, 2020) through 2024. Not a BLS unemployment measure. |
| `INC1` / `INCOME` | Annual household pretax income: 1 under $25k, 2 $25k–34,999, 3 $35k–49,999, 4 $50k–74,999, 5 $75k–99,999, 6 $100k–149,999, 7 $150k–199,999, 8 $200k+. | Present in Week 1 onward, but reference year changes. For 2024, English questionnaires in Phases 4.0, 4.1, 4.2 say **2023**. The Cycle 1 dictionary retains stale “2021” wording; Cycle 9’s dictionary says 2023. Document this conflict rather than silently assigning current-year income. |
| `FD6_NEW` / `FDBENEFIT1` | SNAP/Food Stamp receipt by respondent or someone in household; checkbox selected = 1. | Dictionary identifies Phase 3.7 onward, beginning Dec 9, 2022; verified in Week 63 and all 2024 files. `-99` means question seen but checkbox not selected, not automatically missing or a confirmed binary “No.” `-88` is missing. Reserved as an optional filter pending a careful checkbox-denominator decision. |
| `TBIRTH_YEAR`, `ABIRTH_YEAR` | Year of birth; allocation flag 1 imputed, 2 not imputed. | Birth year present from Week 1; 2024 values are coded to 1936–2006. Use broad approximate age groups. Do not publish birth year in browser data. |
| `EEDUC`, `RRACE`, `RHISPANIC`, `EST_ST` | Educational attainment, race recode, Hispanic origin, state FIPS. | Observed throughout inspected HPS files. Categories and question context change; use age/income/work as the initial demographic filters. Do not assume the current gender or race instrument is unchanged across all phases. |
| `ANXIOUS`, `WORRY`, `INTEREST`, `DOWN` | Anxiety/depression symptom-frequency items; codes 1–4. | Present in inspected Week 1 and 2024; 2024 reference period is two weeks. Earlier pandemic instruments use different recall periods, so do not append a single mental-health trend without harmonization. Core output uses `ANXIOUS` alone and labels it precisely. |
| `PWEIGHT`, `HWEIGHT` | Person/adult and household weights. | Person weights are available in all inspected releases; household weighting arrangements differ in early Phase 1. All 2024 files have both, with 80 person replicates in companion files. Use `PWEIGHT` for the selected adult-percentage estimand. |

The selected 2024 numeric codes are read as integer columns; weights are real-valued numeric columns. State FIPS becomes a zero-padded two-character string. Negative codes are not actual measurements. In the 2024 CSVs inspected, `-88` denotes missing/did not report and `-99` question seen without a response selection. Early dictionaries sometimes describe missing as `.m`; inspect the CSV encoding rather than treating its negative codes as valid values. Exact observed distributions are in `audit/missingness.csv`.

**Observed nonresponse examples:** Cycle 1 has 7,447 invalid/missing `EXPNS_DIF` responses (10.9%), 6,236 `SOCIAL2` (9.1%), and 11,558 `INCOME` (16.9%). Cycle 9 has 2,931 (5.7%), 1,165 (2.3%), and 7,736 (15.1%), respectively. All these selected 2024 fields encode missingness numerically rather than as empty cells. Treating “no blank cells” as “no missing data” would be wrong.

Questionnaire placement also changes: Phases 4.0/4.1 show first/second social question placements, and Phase 4.2 notes removal of `SOC1_second`/`SOC2_second`. The PUF provides the combined `SOCIAL1`/`SOCIAL2` columns. Preserve phase boundaries and item-nonresponse diagnostics when displaying changes; unchanged labels alone do not prove measurement conditions are identical. [Phase 4.2 user notes](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-2_2024_Household_Pulse_Survey_User_Notes_09122024.pdf)

SNAP concepts should not be silently backcast: the inspected 2020 Week 13 file includes a spending-source SNAP checkbox (`SPNDSRC8`), which asks about using a source to meet spending needs, not the same current participation question as `FDBENEFIT1`.

### 4.4 BRFSS: verified potential and added complexity

The latest year listed on the CDC annual-data page is **2025**. Downloaded and streamed every record in `LLCP2019ASC.zip` and `LLCP2025ASC.ZIP`. ASCII records have no header; the official codebook supplies names and fixed-width locations. Actual counts: **418,268** and **356,158**. Actual record widths: 2,158 and 2,066 characters. Only selected fields were decoded; this is not a full all-variable quality audit.

| Year | Full-file rows | Evidence status | Income field in official codebook | Geographic participation / notable issue |
|---|---:|---|---|---|
| 2019 | 418,268 | Measured raw file; codebook read online. | `INCOME2` | 49 states + D.C., Guam, Puerto Rico; New Jersey absent. |
| 2020 | 401,958 | Publisher-reported; codebook downloaded and read. | `INCOME2` | 50 states + D.C., Guam, Puerto Rico. |
| 2021 | 438,693 | Publisher-reported; codebook downloaded and read. | `INCOME3` | 49 states + D.C., Guam, Puerto Rico, U.S. Virgin Islands. |
| 2022 | 445,132 | Publisher-reported; codebook downloaded and read. | `INCOME3` | 50 states + D.C. and the listed territories; corrected colorectal-screening variables in Nov 2023 update. |
| 2023 | 433,323 | Publisher-reported; codebook downloaded and read. | `INCOME3` | Kentucky and Pennsylvania absent; publisher describes later content removal and related missingness. |
| 2024 | 457,670 | Publisher-reported; codebook downloaded and read. | `INCOME3` | Tennessee absent; publisher describes removed content and related missingness. |
| 2025 | 356,158 | Measured raw file; codebook downloaded and read. | `INCOME3` | California, Mississippi, Nevada absent; 47 states + D.C., Guam, Puerto Rico. |

[CDC annual index and year-specific documents](https://www.cdc.gov/brfss/annual_data/annual_data.htm), [2019 codebook](https://www.cdc.gov/brfss/annual_data/2019/pdf/codebook19_llcp-v2-508.HTML), [2025 release](https://www.cdc.gov/brfss/annual_data/annual_2025.html)

`MENTHLTH` and `EMPLOY1` are present in the 2019 online codebook and every downloaded 2020–2025 codebook. `MENTHLTH` measures mentally unhealthy days in the past 30 days: 1–30 days, **88 = zero days**, 77 don’t know, 99 refused, blank not asked/missing. Decode 88 before averaging. Do not turn 77/99 into day counts. There are 8,779 invalid/missing mental-day responses in 2019 and 6,484 in 2025, measured from the downloaded records.

`EMPLOY1` codes 1 employed for wages, 2 self-employed, 3 out of work for a year or more, 4 out of work for less than a year, 5 homemaker, 6 student, 7 retired, 8 unable to work; 9 refused, plus blank. This is not identical to the BLS active-search definition. `INCOME2` has eight bands ending at $75,000+, while `INCOME3` expands the upper bands to 11 categories ending at $200,000+. Harmonize common broad thresholds if used; never append the codes without recoding. `INCOME3` has 71,050 invalid/missing records in the downloaded 2025 data.

`_AGEG5YR`, `_STATE`, `_LLCPWT`, `_STSTR`, and `_PSU` provide age category, state, adult weight, strata, and primary sampling unit. Use annual design-based estimates with the proper weight/design. A file-month or interview-date field does not by itself justify precise monthly state estimates. Geography includes state and metropolitan/urban indicators; these are not county FIPS identifiers. A national annual trend requires a stable geographic universe or explicit coverage qualifications.

BRFSS does have some **direct** social measures: `EMTSUPRT` appears in the inspected 2022–2025 codebooks, and `SDLONELY` in 2023–2025. They are optional-module content, not a uniform national 2019–2025 loneliness series. The 2025 file has 248,391 missing/invalid `SDLONELY` records and 249,164 missing/invalid `EMTSUPRT` records, including structural nonparticipation. Annual codebook presence does not imply every state asked an item. `MENTHLTH` remains a separate concept and is never used as a substitute for loneliness.

An optional BRFSS–LAUS join would aggregate adults by state and survey year, restrict to a common state set, then join to NSA annual `M13` LAUS values through state FIPS and year. It is structurally feasible but has not been executed here. It would add a separate annual narrative and a second survey-design workflow without filling the early direct-loneliness gap.

### 4.5 LAUS: actual files and coverage

Opened the official bulk metadata and two statewide observation files: `la.data.2.AllStatesU` (NSA) and `la.data.3.AllStatesS` (seasonally adjusted). The canonical `download.bls.gov` observation-file route returned HTTP 403 in the downloader. The official **`downloadt.bls.gov`** route succeeded. Also downloaded BLS’s official statewide Excel ZIP alternatives; these were inspected for structure but are not needed in the final combination.

Measured bulk row counts are **235,733 NSA observations** and **186,930 adjusted observations**. These include years/areas outside the project; they are long-form series observations, not individual people. The files served in this audit run end at **March 2026**, although the live BLS site lists later releases. This is a reproducible official-file snapshot, not a claim to possess the latest revisions. Hashes identify its exact bytes. Both selected historical endpoints are present.

Raw columns are `series_id`, `year`, `period`, `value`, `footnote_codes`. Join to `la.series` on the stripped `series_id` to obtain `area_type_code`, `area_code`, `measure_code`, `seasonal`, `series_title`, and beginning/end periods. Statewide areas use type A and `ST` area codes; extract the following two digits as state FIPS. All geographic selections are checked against metadata, not inferred from a state name.

For the 51 jurisdictions and four core measures, the 2019–2025 NSA selection has **18,564 raw long observations**, including 204 unavailable October 2025 cells (51 × 4) and 204 annual cells carrying `G,R` footnotes. The adjusted selection has 17,136 observations, also including the 204 missing October cells. For 2019–2024, all 51 × 72 months × 4 measures are available in each adjustment selection. Published rates are percent with one decimal; counts are persons, **not thousands**. `M13` means annual average and is only used from NSA data. [LAUS bulk dictionary](https://download.bls.gov/pub/time.series/la/la.txt)

Preserve `X` (shutdown unavailable), `G` (2025 eleven-month average), `R` (revision notice) and other flags. Missing “-” values become null, never zero. No county data were downloaded for the core project; LAUS has a county program, but that does not supply county identifiers or county survey outcomes to HPS.

## 5. Candidate evaluation tables

### Candidate A — CDC BRFSS

| Criterion | Evidence-based evaluation |
|---|---|
| Access | Public annual ZIPs with ASCII fixed-width or SAS XPT; no account/key for bulk download. Actual 2019 and 2025 ASCII files opened. Some HTML pages/SAS scripts returned 403 to the local downloader; the 2019 codebook was read through the web tool. No numeric bulk rate limit was verified; cache files and avoid repeated requests. |
| Coverage | Annual 2019–2025 documentation inspected; raw endpoints decoded. State participation changes; territories are outside the intended HPS common universe. Direct social modules cover selected later years/states, not a pandemic-wide national series. |
| Granularity | Adult survey response; state, demographics, annual survey period. Usable drill-down state → age/employment/income. Core aggregate file does not justify a universal county path. |
| Documentation | Year-specific codebooks, fixed-width positions, questionnaires, weighting and comparability documents. Income-field transition and optional modules need harmonization. Current publisher warnings about removed content must be retained. |
| Collection method | Self-reported landline/cellphone survey of adults; complex survey sampling and raking. Repeated annual cross-sections, not longitudinal follow-up of the same people. |
| Bias and gaps | Coverage/nonresponse, self-report and recall error, missing states, optional module participation, changing income bands, and structural missingness. Annual weighted distress estimates do not establish loneliness or pandemic causation. |
| License | CDC BRFSS FAQ explicitly permits dissemination of graphs/tables derived from public-domain federal data and requests CDC BRFSS attribution. Publish derived aggregates with source links; do not use agency marks as endorsement. [BRFSS reuse FAQ](https://www.cdc.gov/brfss/about/brfss_faq.htm) |

### Candidate B — Census HPS

| Criterion | Evidence-based evaluation |
|---|---|
| Access | Official CSV ZIP bulk downloads, including replicates and Excel dictionary; no key/login used. Nine 2024 archives successfully downloaded. A numeric bulk rate limit was not documented/verified; use cached versioned files. The published-table API is unnecessary for custom group comparisons. |
| Coverage | Original HPS begins Apr 23, 2020; inspected representative files for every year 2020–2024, all 2024 cycles, and February 2025 HTOPS. Core social window is Jan 9–Sep 16, 2024, 50 states plus D.C. No original HPS pre-pandemic baseline. |
| Granularity | Responding adult and household reports; state, selected metro, region and demographics. Strong US → state → group path and cycle drill-down. No comprehensive county or daily interview data. |
| Documentation | Dictionaries inside each actual ZIP; phase questionnaires, Source and Accuracy PDFs, user-note corrections. Verified questionnaire/CSV name mapping and response codes. Found and documented Cycle 1 income reference-year inconsistency. |
| Collection method | Experimental rapid internet self-report survey recruited from address records linked to phone/email contacts; adult and household weights, plus successive-difference replicate variance estimation. October 2024/2025 successor uses a new panel design, mailed recruitment, incentives, and telephone option. |
| Bias and gaps | Very low unit response, selective internet/contact coverage, self-report, substantial item nonresponse, instrument/context changes, and small state subgroups. Weighting cannot guarantee removal of nonresponse bias. Census reports weighted response 6.5% for Cycle 1 and 4.7% for Cycle 9. |
| License | Public-use files are released by Census for custom tabulation. Census DS027 p.9 states Census employee works generally have no U.S. copyright protection, while noting contractor/foreign exceptions. No file-specific visualization prohibition was found in the inspected PUF material. Derived factual aggregates with attribution are suitable for the proposed U.S. course site; do not claim a blanket CC0 license for every Census artifact. [PUF purpose](https://www.census.gov/programs-surveys/household-pulse-survey/data/datasets.html), [DS027 policy](https://www2.census.gov/foia/ds_policies/ds027.pdf) |

### Candidate C — BLS LAUS

| Criterion | Evidence-based evaluation |
|---|---|
| Access | Public tab-delimited bulk observations plus metadata, and official Excel ZIP alternatives. No key used. Canonical bulk host gave 403 for some files; official alternate host worked. API limits are irrelevant to the selected bulk route and were not tested. |
| Coverage | Downloaded snapshot spans 1976–Mar 2026; retained 2019–2025, with 2019–2024 the complete comparable core. 50 states + D.C.; exclude Puerto Rico/territories to match HPS. October 2025 unavailable and 2025 annual averages incomplete. |
| Granularity | One series × period observation; pivot to state × month/year. Year → month drill-down. Counties exist in a separate LAUS product but are unnecessary and were not downloaded. No individual demographics in the statewide time series. |
| Documentation | `la.txt`, `la.series`, `la.measure`, `la.area`, `la.footnote`; units, adjustment, area and period definitions inspected. State-rate counts and all selected series keys checked. |
| Collection method | State estimates are model-based, combining CPS, employment statistics, administrative information, and benchmark controls; not a census of workers. Measures are by residence, not job location. |
| Bias and gaps | Model uncertainty, revisions/benchmarking, adjustment choice, population-control changes, and missing 2025 collection. Lower unemployment may coexist with a changing labor-force denominator. |
| License | BLS explicitly places its published material in the public domain except previously copyrighted photographs/illustrations; asks users to cite BLS. Public derived charts and static data are permitted. Do not use the BLS emblem without authorization. [BLS copyright policy](https://www.bls.gov/opub/copyright-information.htm) |

These are two independent **data-generating programs** in the selected combination: HPS respondent survey and LAUS statistical estimates. BLS participates in HPS content development and uses Census population controls in LAUS, so “independent sources” does not mean statistically independent estimates. CDC’s republished HPS tables do **not** count as an additional independent respondent source.

## 6. Question coverage matrix

“Fully supported” means the inspected source supplies the measures at the stated scope, not that every analysis or significance test has already been completed.

| Candidate | Q1 Labor recovery | Q2 Labor–hardship join | Q3 Work × income hardship | Q4 Hardship, loneliness, anxiety | Q5 State-age social support |
|---|---|---|---|---|---|
| BRFSS | Partially supported: annual self-reported work status, not monthly LAUS recovery statistics. | Partially supported: state/year and employment context; no identical 7-day HPS expense outcome. | Partially supported: work and income, but the expense metric is different. | Partially supported: later optional loneliness and mental-day measures; no equivalent core anxiety item or uniform state coverage. | Partially supported: later optional support/loneliness and age, with state/module gaps. |
| HPS | Not supported: no 2019 baseline or official LAUS series. | Partially supported: hardship, geography and period; lacks LAUS unemployment context. | Fully supported in 2024. | Fully supported in 2024. | Fully supported within 2024, subject to small-cell reliability. |
| LAUS | Fully supported for 2019–2024. | Partially supported: labor measures and keys; no hardship outcomes. | Not supported. | Not supported. | Not supported. |
| HPS + LAUS, selected combination | Fully supported. | Fully supported after state-FIPS/period alignment. | Fully supported through HPS. | Fully supported through HPS. | Fully supported through HPS. |

Q2 explicitly requires the independent-source join. Q1 establishes the economic context that Q2 tests against household experience. Q3–Q5 explain which people/groups lie behind state averages, using respondent relationships only within HPS. Thus the sources form one coherent account rather than disconnected charts. No person in BRFSS is linked to a person in HPS.

## 7. Joining and preparation strategy

### 7.1 Executed workflow

1. Download official archives and metadata; record filenames, URLs, bytes, retrieval date and SHA-256. Preserve raw ZIPs privately. Extract selected survey columns directly from the ZIPs.
2. Validate survey code sets; distinguish blank, `-88`, `-99`, valid zero, and structural nonparticipation. Treat `SCRAM` as a string, never as a quantity or a public identifier. For the main HPS estimands, exclude invalid responses from each outcome’s denominator and retain the exclusion count.
3. Match each cycle’s respondent records to its **own** replicate file through `SCRAM`, requiring unique keys and one-to-one matching. All nine cycles matched completely; all 80 person replicate columns were present. This is an internal same-survey weight join, not the independent-source assignment join.
4. Compute weighted state and national percentages, first overall and then for declared age, work, income, work/income, hardship, and support groups. Do not join respondents to repeated monthly BLS rows before aggregation.
5. Strip whitespace from BLS headers/keys; attach area/measure metadata through `series_id`, requiring a many-to-one metadata match. Select statewide type A, 50 states + D.C., four measures, and intended years. Preserve seasonal adjustment, missing flags and annual-period status. Check employment plus unemployment approximately equals labor force (rounding tolerance at most 2 people).
6. Convert each HPS interval to a unique state-cycle BLS context record using the month-overlap bridge below. Join on `state_fips, cycle`, requiring **one-to-one** for overall state estimates. Demographic aggregates use a **many-to-one** join to the same contextual record; BLS is not suddenly a demographic unemployment estimate.

### 7.2 Weights and uncertainty

For valid outcome indicator y and adult weights w, calculate `p = sum(w*y) / sum(w)`. For Q2, this estimates the share of adults reporting difficulty in their household; it is **not** the percentage of households. A household-percentage chart would require `HWEIGHT` and a clearly different estimand.

For every main estimate, calculate the same ratio under each of the 80 person replicate weights. Use Census’s successive-difference replication formula: `variance(p) = (4/80) * sum((p_r - p)^2)`. The supplied output includes sampling SE in percentage points and a 90% normal interval, clipped to 0–100. These intervals do not cover all nonresponse, coverage, measurement, or model error. [Cycle 9 Source and Accuracy, pp.13–14](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-2_Source_and_Accuracy_Cycle09.pdf)

The prototype rule suppresses an estimate when its valid unweighted n is below 100 or Kish effective n is below 30. This is a **project rule**, not official NCHS certification. Suppressed percentages, numerators and intervals are blank in the exported products. Each metric has its own valid n, missing n and suppression flag. Across 8,892 exported aggregate rows, 848 loneliness estimates are suppressed. Start with broad groups; do not implement unrestricted combinations of all filters.

Some rows conditioned on hardship or support also contain that same metric, producing a definitional 0% or 100%. These are not discoveries; the dashboard should disable an outcome when its group filter defines the outcome itself. To test a gap, compute the gap within each replicate and then its variance; this task exports individual group intervals, not a full table of gap tests. Between-cycle tests also require checking overlap/dependence rather than assuming independent samples.

### 7.3 Temporal alignment actually implemented

HPS cycles overlap calendar months. Cycle 1 spans January 9–February 5: 23 days in January and 5 in February. For each state, form day-weighted unemployment and labor-force counts across those months, then compute `100 * aligned_unemployed / aligned_labor_force`. Employment and labor-force counts remain average contextual levels, not summed person counts. This avoids averaging rounded monthly rates and does not duplicate respondents.

This is a **declared alignment approximation**: LAUS is not observed daily, its reference concepts do not equal a daily stock, and HPS’s seven-day recall windows can reach before a cycle starts. The bridge aligns collection windows, not individual recall dates. A simpler sensitivity analysis should compare the midpoint-month rate; a production conclusion should not depend on that alignment choice. `period_month_bridge.csv` contains the executed fractions. The code also constructs a 2019 comparison using the same calendar-month mixture; no HPS data are imputed into 2019.

Use NSA LAUS for the cross-sectional HPS context and seasonally adjusted LAUS for standalone monthly recovery curves. For annual work, use published NSA `M13`. Do not average the nine 2024 HPS cycles and label the result a full-year estimate: they cover January 9–September 16 only. The primary dashboard needs no survey pooling.

### 7.4 Join results and resulting tables

| Check | Executed result |
|---|---:|
| HPS 2024 raw respondent records | 610,755 |
| HPS overall state-cycle keys | 459 |
| LAUS aligned state-cycle keys | 459 |
| Left join output rows | 459 |
| Unmatched left / right keys | 0 / 0 |
| Duplicate state-cycle keys before join | 0 |
| State demographic-context rows checked | 8,721 |
| Unmatched demographic-context rows | 0 |
| All HPS national/state/group output rows | 8,892 |
| LAUS state-month rows, 2019–2025, both adjustment statuses | 8,568, including 102 unavailable October rows after pivot |

`joined_state_cycle_2024.csv` is a preliminary joined **aggregate** dataset. Each row contains weighted HPS estimates, valid sample sizes, SEs/intervals, and aligned BLS contextual counts/rates. `hps_2024_aggregates.csv` includes the national and demographic samples. `laus_state_month_2019_2025.csv` and the separate annual file support the longer recovery context; filter out 2025 for the complete-year core.

The assignment size condition is satisfied by the measured HPS respondent files alone. Including the selected 2019–2025 NSA BLS long records gives 629,319 input rows, but 204 of those BLS cells are unavailable. Even using only 2019–2024 complete BLS observations, there are **626,667** selected input records. Weight-companion rows, additional adjustment versions, BRFSS, and joined output rows are unnecessary to reach 50,000.

## 8. Independent checks and preliminary evidence

Four national weighted numerator/denominator checks—support and loneliness for Cycles 1 and 9—were compared with the original Census Health Table 6a workbooks. All agree within **one person**, consistent with the official table’s rounding. This independently checks the weight choice, valid denominator, question coding and file interpretation. The comparison details are preserved in `audit/independent_validation.json`.

As an exploratory example from Cycle 9 (August 20–September 16):

| Adult group defined by expense difficulty | Frequent loneliness | Frequent anxiety |
|---|---:|---:|
| Not at all / a little difficult | 8.2% | 9.7% |
| Somewhat / very difficult | 21.0% | 26.9% |

These are weighted percentages among valid outcome responses in each group. They show that the proposed group comparisons contain information worth visualizing. They do not establish direction of influence, a pandemic effect, or a statistically adjusted relationship. Do not turn this table into the final authored conclusion until the team reviews uncertainty, subgroup composition, missingness and the other cycles.

Overall frequent loneliness is estimated at 13.3% in Cycle 1 and 13.0% in Cycle 9. This small descriptive difference is **not evidence of a meaningful decline**; sampling error and changing nonresponse/context must be assessed. Keep the full response distribution accessible so conclusions do not depend only on one dichotomy.

## 9. Final decision, revisions and limitations

**Retain HPS + LAUS.** They directly connect household hardship and social well-being with state labor-market context, supply a large raw sample, have usable shared state/time keys, and permit public factual aggregate visualizations. Their preparation has been executed successfully. The team can limit itself to one respondent survey design and one small economic time series.

**Reserve BRFSS.** It is high-quality and useful for annual mentally unhealthy days before and after the disruption, but it adds an independent questionnaire/weighting pipeline, state coverage changes, income harmonization, and optional social-module gaps. It does not fix the lack of a nationally comparable 2019 loneliness baseline. Add it only if the team explicitly replaces one current question with an annual mental-health question. No fourth or international source is needed to make the selected pair feasible; ACS/ATUS/WVS were therefore not expanded into an unnecessary additional acquisition effort.

The original ideas were revised as follows:

| Initial idea | Decision based on evidence |
|---|---|
| Loneliness before, during and after COVID | Drop the implied historical change claim. Analyze direct HPS loneliness only in 2024. |
| Economic recovery through a complete 2025 | Use 2024 for complete annual comparison; flag 2025’s missing October/11-month annual averages. |
| Continuous HPS–HTOPS trend | Reject for the core dashboard. The inspected successor is national, redesigned, and uses different fields/content. |
| Link people across CDC and Census | Reject. Join aggregate state/time contextual records only. |
| State → county → demographic dashboard | Replace with US → state → broad group. HPS lacks comprehensive county geography. |
| Psychological distress as loneliness | Reject. Keep mentally unhealthy days, anxiety symptoms, needed support and loneliness distinct. |
| SNAP recipients versus everyone else as a binary | Reserve. Checkbox nonselection and item missingness need an explicit denominator; it is not essential to the five core questions. |

Remaining limitations are substantive. HPS excludes people outside its covered household population and has very low response; demographic weighting cannot guarantee unbiased outcomes. Income is lagged and missing for many respondents. State groups have unequal sample sizes, with some suppressed. Age is approximate. State unemployment relates to a different age/population universe than HPS adults. LAUS is modeled and revised. A low unemployment rate can reflect labor-force changes, not universal security. State associations are ecological and cannot identify an individual’s unemployment exposure. The surveys do not isolate pandemic effects from inflation, policy, age composition, longstanding inequality, or other concurrent changes.

The inspected HPS Phase 4.1 user note also documents a gender/sexual-orientation experiment that increased missingness in Cycles 1–5. The proposed core filters avoid these fields; an expansion must revisit those notes. BRFSS current release notices describe content removal in 2023/2024, another reason to pin versions and read current documentation instead of assuming old schemas survive unchanged.

**Privacy and public display:** No names, addresses, contact information or direct personal identifiers were found among the selected analytical fields. `SCRAM`, `SCRAMID`, `_PSU`, sequence numbers, exact birth year and exact interview dates are excluded from the public analytical exports. The core package publishes HPS aggregates only. A 100-row BRFSS convenience sample contains only state, file month and mental-day response/cleaned value; it is for parsing illustration, not population inference. Prefer the aggregate BRFSS example for public charts. Do not upload raw source ZIPs or replicate files to the public website, even where redistribution is permitted; they are unnecessary and enlarge disclosure exposure and download size.

## 10. Dashboard feasibility and static preparation

Build three linked views with a short authored sequence:

1. **Recovery context:** annual 2019/2024 state comparison and monthly LAUS curves, with a clear 2020 reference band. Use the complete period for the main narrative; show 2025 only with a visible gap and incomplete-year label if retained.
2. **Recovery versus lived hardship:** state-cycle scatterplot of unemployment versus hardship, linked to a state choropleth and cycle selector. Clicking a state opens its group comparisons. Explain exactly what the independent-source join adds.
3. **Who remains under strain:** paired or grouped bars for hardship by work/income and loneliness/anxiety by hardship, plus an age view for support/loneliness. Show weighted percentages, valid n, uncertainty, missingness and suppression states in tooltips or an accessible data table.

Begin with a neutral authored claim such as “Labor-market recovery is one part of household well-being.” After the team completes Q1–Q5, write two or three specific, quantified conclusions, allow state/group selection to test them, and link a methodology view. Do not begin with a causal claim that COVID increased loneliness.

Use a static frontend such as D3 or Vega-Lite with plain JavaScript. No server or browser-side survey statistics are required. Perform raw downloads, weighting, grouping, variance calculations and joins offline. Publish only small CSV/JSON files and a compact state boundary file from an appropriate original source when building the map. Geography for the map has not yet been acquired; it is a presentation dependency, not needed for the validated analytical join.

The delivered HPS aggregate CSV is about **3.59 MB**, the joined state-cycle CSV about **246 KB**, and the two-adjustment LAUS monthly CSV about **554 KB**. These are feasible static downloads. A production export can drop unused diagnostic columns, round chart percentages to 1–2 decimals, and split demographic files by state. Retain a compact metadata dictionary, numerator/denominator definitions, cycle boundaries, uncertainty and source/version links. A label such as “18–34, worked, under $50k” is possible only when that exact grouping has been computed; the current sample supports declared one-way groups plus work × income, not arbitrary intersections.

Realistic preparation effort is moderate: a few focused sessions for the team to rerun the supplied workflow, inspect the audited distributions, choose reliability/denominator rules, and finish analysis. The difficult part is honest survey interpretation rather than file joining. Keep that scope intact instead of adding county or international reconciliation.

## 11. Assignment compliance and team next steps

| Professor requirement | Status and evidence |
|---|---|
| At least two independent sources, joined | Satisfied: Census HPS + BLS LAUS; executed 459-row state-cycle join. |
| Approximately 50,000 raw rows | Satisfied: 610,755 measured core HPS records alone. |
| Temporal attribute | Satisfied: year/month and dated HPS collection cycles. |
| Two categorical/geographic attributes | Satisfied: state FIPS, age group, work status and income category. |
| At least three quantitative attributes | Satisfied: unemployment rate, employment, unemployment and labor-force counts, plus hardship/loneliness/support/anxiety percentages. |
| Meaningful drill-down | Satisfied by actual records: US → state → age/work/income group and year → month/cycle. No county capability claimed. |
| Original source | Satisfied: official CDC, Census and BLS downloads/documentation; no aggregator data used. |
| Public visualization rights | Verified for the proposed derived factual aggregates through agency policies and public-use release documentation; preserve attribution and distinguish original analyses from agency publications. |
| No published PII | No direct identifiers in supplied analytical exports; raw files kept out of public package. Recheck the eventual site/repository before publishing. |
| 3–5 measurable questions and notes | Satisfied: five exact questions, each with four notes. |
| Three candidate evaluations / coverage matrix | Satisfied in Sections 5–6. |
| Decision and AI disclosure | Satisfied in Sections 9 and 12. |
| Authored narrative plus interactive exploration | Data support it; implementation deliberately not started in this task. |

No core acquisition or join requirement is awaiting evidence. Remaining decisions are implementation/analysis tasks: choose the final reliability presentation rule, finish confidence-aware group-gap analysis, test sensitivity to temporal alignment and missing responses, obtain map boundaries, and verify the final public build contains only aggregate outputs.

**Exact next steps:**

1. Download the evidence package, read the report and `README.md`, and assign one teammate to rerun the acquisition/preparation code using the manifest. Confirm the hashes or explicitly re-audit changed publisher files.
2. Agree on the 2019–2024 labor baseline, 2024 HPS window, adult estimand, broad group definitions, and missingness/suppression policy. Keep SNAP and HTOPS out of the minimum scope.
3. Complete Q1/Q2 and Q3–Q5 in parallel within the team, review all reported values against denominators and intervals, and retain counterexamples to the narrative. Add replicate-based differences before labeling gaps significant.
4. Create a small production export from the audited aggregate tables, with metadata, and verify no respondent-level or weight files enter the public repository.
5. Build the three views and authored sequence, test state/group drill-downs including suppressed cells, then publish on GitHub Pages after the team reviews the findings and sources.

## 12. AI-use disclosure

AI proposed a narrower HPS + LAUS design, research questions, a period-overlap alignment, broad groups, and a static-data architecture. Those choices are recommendations, not professor requirements or agency standards. AI wrote and executed acquisition, inspection and aggregation code and drafted this report.

What was independently checked against real source evidence: official publisher pages and current year lists; actual archive contents and CSV headers; all nine 2024 respondent and replicate files; representative HPS files in 2020, 2021, 2022 and 2023; a 2025 HTOPS file; BRFSS raw endpoints and intervening codebooks; LAUS series/area/measure/footnote metadata; missing codes and counts; raw row totals; aggregate join cardinality; and four weighted estimates against original Census tabulations. “Independently checked” here means a separate official tabulation or source document was used; it does not mean an independent human auditor has reviewed the project.

Ideas rejected or corrected after verification: CSV columns named literally `SPN4`, `SOC1`, `SOC2`; early-pandemic HPS loneliness; continuous state HPS–HTOPS comparability; a complete 12-month 2025 labor baseline; mental-health days as loneliness; checkbox negatives as uniformly missing; unweighted survey percentages; household percentages calculated with person weights; and person-level cross-survey joins. The Cycle 1 income-dictionary conflict was resolved for this project using three official 2024 phase questionnaires and the Cycle 9 dictionary, with the discrepancy retained.

Downloads that failed are logged with their errors. ZIP content that the web-reading tool could not display was retrieved using the file downloader and actually opened. The failed 2019 BRFSS HTML download was supplemented by reading the official codebook through the web tool. Failed guessed URLs were not cited as inspected files. No correlation, statistical significance result, causal estimate, or undownloaded raw row count is represented as measured.

## 13. Original-source reference guide

The machine-readable `download_manifest.json` records exact successful download URLs, actual filenames, file sizes and hashes. `audit/dataset_audit.csv` is the detailed file-level technical table; `audit/download_attempts.json` also retains failures. Important sources are:

| Source | Original-publisher reference and role |
|---|---|
| BRFSS annual index | [CDC annual data](https://www.cdc.gov/brfss/annual_data/annual_data.htm): 2019–2025 release pages, codebooks, participation and file counts. |
| BRFSS raw endpoints | [2019 ASCII ZIP](https://www.cdc.gov/brfss/annual_data/2019/files/LLCP2019ASC.zip), [2025 ASCII ZIP](https://www.cdc.gov/brfss/annual_data/2025/files/LLCP2025ASC.ZIP). |
| BRFSS response definitions | [2019 codebook](https://www.cdc.gov/brfss/annual_data/2019/pdf/codebook19_llcp-v2-508.HTML), [2025 codebook ZIP](https://www.cdc.gov/brfss/annual_data/2025/zip/codebook25_llcp-v2-508.zip). |
| HPS file index | [2024 Census PUFs](https://www.census.gov/programs-surveys/household-pulse-survey/data/datasets.2024.html); use year selectors for historical releases. Dictionaries accompany the exact archives. |
| HPS example core files | [Cycle 1 CSV ZIP](https://www2.census.gov/programs-surveys/demo/datasets/hhp/2024/cycle01/HPS_Phase4Cycle01_PUF_CSV.zip), [Cycle 9 CSV ZIP](https://www2.census.gov/programs-surveys/demo/datasets/hhp/2024/cycle09/HPS_Phase4-2Cycle09_PUF_CSV.zip). |
| HPS instruments | [2024 questionnaires](https://www.census.gov/programs-surveys/household-pulse-survey/technical-documentation/questionnaires.2024.html). |
| HPS uncertainty | [Cycle 1 Source and Accuracy](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-0_Source_and_Accuracy_Cycle01.pdf), [Cycle 9 Source and Accuracy](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Phase4-2_Source_and_Accuracy_Cycle09.pdf). |
| HPS corrections/redesign | [2024 user notes](https://www.census.gov/programs-surveys/household-pulse-survey/technical-documentation/user-notes.2024.html), [October 2024 methodology](https://www2.census.gov/programs-surveys/demo/technical-documentation/hhp/Source_and_Accuracy_October_2024_FINAL.pdf). |
| Independent estimate check | [Census Cycle 1 Health 6a](https://www2.census.gov/programs-surveys/demo/tables/hhp/2024/cycle01/health6a_cycle01.xlsx), [Cycle 9 Health 6a](https://www2.census.gov/programs-surveys/demo/tables/hhp/2024/cycle09/health6a_cycle09.xlsx). |
| Social indicator definitions | [CDC HPS lack of social connection](https://www.cdc.gov/nchs/covid19/pulse/lack-socialconnection.htm); derived from HPS, not an independent extra source. |
| LAUS official access | [BLS LAUS data](https://www.bls.gov/lau/data.htm), [canonical bulk directory](https://download.bls.gov/pub/time.series/la/), [successful official NSA bulk URL](https://downloadt.bls.gov/pub/time.series/la/la.data.2.AllStatesU). |
| LAUS definitions | [Bulk dictionary](https://download.bls.gov/pub/time.series/la/la.txt), [state estimates overview](https://www.bls.gov/lau/rdscnp16.htm), [2025 missing-month/revision notice](https://www.bls.gov/lau/launews1.htm). |
| Reuse conditions | [BRFSS FAQ](https://www.cdc.gov/brfss/about/brfss_faq.htm), [BLS public-domain policy](https://www.bls.gov/opub/copyright-information.htm), [Census DS027 p.9](https://www2.census.gov/foia/ds_policies/ds027.pdf). |

## Deliverable D — Recommendation summary

**Use Census HPS 2024 Cycles 1–9 plus BLS LAUS 2019–2024.** Keep flagged 2025 LAUS data only as an optional extension. Reserve BRFSS; exclude HTOPS from the core. The selected pair is accessible, already joined, large enough, and suited to state/demographic exploration.

The five strongest feasible questions are: **(1)** which states recovered in labor-market terms; **(2)** whether low unemployment coincides with low hardship; **(3)** how work/income groups differ in hardship; **(4)** how hardship groups differ in loneliness and frequent anxiety; **(5)** whether national age patterns of support and loneliness hold within states.

All source, raw-size, dimensional, drill-down and tested-join requirements are supported by the acquired evidence. Public factual aggregate display is supported by the publisher policies; the supplied analytical exports contain no direct respondent identifiers. The team still needs to complete the analyses and uncertainty/sensitivity review, acquire presentation map boundaries, and build/test the narrative and interactive site. The report, technical audit, samples and reproduction code provide the foundation for that work.
