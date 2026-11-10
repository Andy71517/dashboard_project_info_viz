# Local execution and validation

Validated on November 10, 2026, against the original source files acquired for this project on November 2, 2026.

The complete notebook executed locally, including every data-preparation cell, in about 5 minutes 44 seconds. The chart and export cells were rerun after correcting currency rendering and limiting the timeline axis to the selected years. The underlying weighted data were unchanged. Machine-specific output-path lines were omitted from the delivered notebook for privacy.

This is local execution evidence. The notebook has not been run inside your Google account. The downloading cell reused the verified local original inputs during this run; the Colab cloud download path was not exercised in your account. The support ZIP supplies the exact BLS snapshot used for the run.

| Check | Actual result |
|---|---|
| Code cells executed without errors | 19 |
| HPS original respondent records | 610,755 |
| BLS unadjusted selected long observations | 15,912 |
| Combined raw observations, excluding the duplicate adjusted version | 626,667 |
| Weighted HPS national/state/group rows | 8,892; overlapping views, not independent respondents |
| BLS monthly state rows | 7,344 |
| BLS annual state rows | 306 |
| State-cycle join | 459 → 459 |
| Unmatched left / right keys | 0 / 0 |
| Cleaning decisions recorded | 208 |
| Notebook checks passed | 216 |
| Random processed cases compared with reloaded original CSV rows | 20 / 20 passed |
| Raw-to-processed field comparisons | 180 passed |
| Exploratory figures | 6; all visually inspected |
| Agreement with prior verified aggregate preparation | All 8,892 rows and suppression flags reproduced |
| Maximum difference from prior six-decimal CSV exports | 0.000000507; consistent with CSV rounding |
| Prior official Census Table 6a benchmarks | Four numerator/valid-denominator comparisons reproduced within one person of published rounded totals |
| Raw respondent fields in public exports | None; raw and private spot-check folders excluded |
| Manual team review | Pending |

The 20-case comparison is automated. The private table is generated when you run the notebook; review it in your own workspace and record the human review separately. It is intentionally absent from this package.

## Preliminary findings for discussion

- 21 of 51 jurisdictions had a published 2024 annual unemployment rate at or below their 2019 rate.
- In Cycle 9, the descriptive state-level Spearman association between aligned unemployment and hardship is 0.10; a midpoint-month alignment gives 0.13.
- The largest absolute midpoint-versus-overlap difference across all state-cycle observations is 0.476 percentage points.
- The group comparison reproduces the earlier Cycle 9 loneliness estimates of about 21.0% versus 8.2%, and frequent anxiety-symptom estimates of about 26.9% versus 9.7%, for harder-to-pay versus easier-to-pay expense groups.

These are descriptive findings. No causal effect or statistically significant group difference is claimed. Survey nonresponse, missing answers, changing samples, lagged income, approximate ages, small groups, and modeled/revised BLS estimates remain limitations.

## Review and source evidence

The notebook includes exact original URLs and input fingerprints. The briefing ZIP includes the executed cleaning log, missingness table, row counts, join checks, source provenance, chart captions, and aggregate data. The BLS support ZIP contains only public aggregate BLS data and metadata, plus the input manifest. It does not contain HPS microdata.

## AI disclosure

AI wrote and ran the notebook, checked its outputs against the previous verified preparation, reproduced four previously checked publisher-table benchmarks, generated the figures, inspected the six rendered figures, and wrote the walkthrough. The team has not yet manually reviewed the 20 cases or approved the interpretation. No stakeholder dialogue has been invented.
