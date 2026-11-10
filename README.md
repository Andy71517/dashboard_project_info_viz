# COVID recovery and household well-being

This is our university information visualization project. We are studying whether employment recovery goes along with less financial hardship and better social well-being, and how those patterns differ across states and groups.

We use **Census Household Pulse Survey (HPS), 2024 Cycles 1–9**, and **BLS Local Area Unemployment Statistics (LAUS), 2019–2024**. BRFSS was evaluated in Part 1 and remains optional. The dashboard has not been built yet.

## Start with the completed notebook

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Andy71517/dashboard_project_info_viz/blob/main/notebooks/COVID_Recovery_Step0.ipynb)

**[View the notebook with saved outputs](notebooks/COVID_Recovery_Step0.ipynb)** · **[Step-by-step walkthrough](docs/START_HERE.md)** · **[Local validation results](docs/LOCAL_VALIDATION.md)**

The notebook contains the complete preparation code, weighted estimates, missingness and cleaning logs, join checks, 20 automated raw-to-processed comparisons, six exploratory charts, and an exportable stakeholder briefing. Its outputs are saved, so the tables and charts can be read before rerunning it.

1. Click **Open in Colab** above and save your own copy in Drive.
2. Download **[Step0_Colab_Support.zip](downloads/Step0_Colab_Support.zip)**. In Colab's Files panel, upload it into `/content` and leave it zipped. This supplies the exact BLS snapshot used in the report.
3. Follow the notebook in order. It can download missing HPS ZIPs from Census, or reuse the original nine ZIPs you already have. The walkthrough explains the Drive option.
4. Review the results and download the generated briefing ZIP. The detailed 20-row table stays in your private workspace for manual team review.

The notebook was executed **locally** against the audited source files. Running it in your Colab account and manually reviewing the 20 cases are still team tasks. The first run needs about 660 MB of HPS downloads unless you supply the original archives. Use a normal CPU runtime; no API key or GPU is required.

## What is included

| Location | Contents |
|---|---|
| [notebooks/](notebooks/) | Complete executed Step 0 notebook with tables and six inline figures |
| [data/processed/](data/processed/) | Aggregate HPS estimates, BLS monthly/annual tables, the tested join, and drill-down/recovery tables |
| [audit/step0/](audit/step0/) | Cleaning decisions, missingness, provenance, checks, counts, alignment sensitivity, and public spot-check summary |
| [reports/step0/](reports/step0/) | Six chart images, captions, and the self-contained HTML briefing |
| [reports/phase1/](reports/phase1/) | Final Word submission and the detailed data research report |
| [docs/](docs/) | Walkthrough, validation notes, and official source dictionaries/methodology |
| [downloads/](downloads/) | Small frozen BLS support ZIP for reproducing our report |
| [scripts/phase1/](scripts/phase1/) | Earlier acquisition/preparation scripts and original download manifest |
| [audit/phase1/](audit/phase1/) | Candidate-source audit, including inspected historical samples and BRFSS |

Download [briefing_pack.html](reports/step0/briefing_pack.html) and open it in a browser to read the initial briefing. Its six chart images are embedded, so it works without a server. GitHub itself may display the HTML source rather than the rendered page. This repository does not automatically deploy a website.

## Verified checkpoints

- **610,755** raw HPS respondent records; **626,667** combined raw observations after adding selected BLS unadjusted long observations without counting the adjusted version twice.
- **8,892** weighted HPS national/state/group rows. These are overlapping views, not independent respondents.
- **7,344** BLS monthly rows and **306** published annual rows for the project scope.
- **459** joined state-cycle rows, with **zero** unmatched keys on either side.
- **208** cleaning decisions and **216** passing notebook checks.
- **20/20** automated raw-to-processed case checks passed, covering **180** field comparisons.
- All 8,892 aggregate rows reproduced the earlier verified preparation. Four previously checked Census published-table benchmarks reproduced within one person of rounded totals.

## Questions guiding the work

1. Which states returned to their 2019 annual unemployment rate by 2024, and how did their monthly paths differ?
2. In each 2024 cycle, do states with lower unemployment also have less reported expense difficulty?
3. How does hardship differ between work groups within three household income bands?
4. How do frequent loneliness and anxiety symptoms differ between hardship groups?
5. How do loneliness and lack of support differ across age groups, and does the national pattern hold within a state?

These are descriptive questions. HPS uses repeated cross-sections and person weights. The direct loneliness and support questions start in January 2024; they do not support a 2020–2024 loneliness trend. Income refers to 2023 household income. Not working in the last seven days is broader than being unemployed under BLS definitions. State associations do not establish individual relationships or causal effects.

## Reproducibility and publication

The BLS support archive is a fixed snapshot retrieved November 2, 2026, rather than a claim to contain the latest release. Exact original URLs and SHA-256 fingerprints are recorded in the input manifests. The notebook stops on unexpected source changes, broken keys, invalid codes, or incomplete scope. An intentional revised BLS run requires review and the notebook's explicit configuration option.

Original HPS respondent files, weight files, and the private case-comparison table are excluded. Only aggregate analytical data and a public pass/fail summary are committed. The notebook's original-source downloads recreate the raw inputs privately. Official agency dictionaries and codebooks are included as documentation. See [data and source notes](docs/DATA_AND_SOURCES.md).

To check the committed project without downloading raw data:

```bash
python scripts/check_repository.py
```

For optional local execution, use Python 3.12 and install `requirements.txt`; the notebook is the main Step 0 workflow. The older Phase 1 scripts have their own requirements and [instructions](scripts/phase1/README.md).

## AI use and review status

AI helped research and inspect the original files, write and run preparation code, create the notebook and charts, and draft the documentation. Automated execution and comparison checks are recorded. Human team review, approval of the interpretation, and stakeholder discussions are still pending. No stakeholder conversation has been invented.
