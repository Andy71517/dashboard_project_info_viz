# Data and source notes

## Selected sources

- **Census HPS:** [2024 public-use files](https://www.census.gov/programs-surveys/household-pulse-survey/data/datasets.2024.html), Cycles 1–9. The original ZIPs include respondent data, dictionaries, and replicate weights. The notebook calculates percentages of adults using PWEIGHT and 80 person replicate weights, with 90% sampling intervals.
- **BLS LAUS:** [official bulk directory](https://download.bls.gov/pub/time.series/la/) and [file documentation](https://download.bls.gov/pub/time.series/la/la.txt). We retain statewide measures 03–06 for the 50 states and D.C., 2019–2024. Rates are percentages; counts are people, not thousands.
- **CDC BRFSS:** [official annual files](https://www.cdc.gov/brfss/annual_data/annual_data.htm). Evaluated as a candidate; not part of the core Step 0 notebook.

The Phase 1 report includes the full candidate evaluation and policy references. Original-source documentation is under `docs/source_documentation/`. Government materials remain attributable to their original publishers; no agency endorsement is implied. The BLS [copyright policy](https://www.bls.gov/bls/linksite.htm) and Census [DS027 policy](https://www2.census.gov/foia/ds_policies/ds027.pdf) support the factual public-display use documented in the report. This repository does not apply a new license to agency materials.

## Analytical units and join

HPS raw records represent individual adult responses within a collection cycle. We aggregate before attaching BLS state context. The main analytical key is `state_fips, cycle`: 459 state-cycle rows. A demographic view can attach the same state context many-to-one; it must not be called that demographic group's unemployment rate.

Collection cycles can span two months. We align unadjusted monthly BLS counts with collection-day overlaps, then derive the unemployment rate. This is approximate context, not observed daily unemployment. The midpoint-month sensitivity table is included. Adjusted monthly series are used separately for the timeline, and published unadjusted M13 values for annual comparisons.

## Missingness, reliability, and privacy

Invalid single-choice responses are removed from the relevant denominator, not replaced with zero. Percentages are on a 0–100 scale; standard errors are in percentage points. Estimates below valid n=100 or Kish effective n=30 are hidden. This is a project rule, not official CDC certification. The aggregate group dimensions overlap and cannot be summed into independent population totals.

No raw respondent rows, respondent IDs, birth years, exact interview dates, or private 20-case comparison are committed. The notebook uses same-survey IDs internally to align weights, then exports aggregates. Its detailed row-comparison file is private and excluded from the briefing export. The committed 20-case summary reports case numbers and pass/fail information only.

## Files and dates

`audit/step0/input_manifest.json` identifies the selected core source snapshot. `audit/step0/input_provenance.csv` records the inputs checked by the executed notebook. The broader Phase 1 manifest is under `scripts/phase1/`. These manifests preserve source dates and successful original URLs, including the official BLS download host that served the audited snapshot.

The core scope ends in 2024. The earlier Phase 1 audit retains evidence about 2025 LAUS missing October and incomplete annual figures; those observations do not enter the main Step 0 outputs. HPS's redesigned successor is also excluded from the core. Historical HPS and BRFSS audit metadata are documentation of candidate inspection, not extra pooled observations in the notebook.
