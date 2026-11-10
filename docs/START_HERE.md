# Run the COVID Step 0 notebook in Colab

This notebook covers the assignment screenshot's **Step 0: clean and explore the data**. It prepares the data and briefing for a stakeholder discussion. It does not invent stakeholder interviews or build the dashboard.

## 1 Open the notebook

1. Download **[COVID_Recovery_Step0.ipynb](../notebooks/COVID_Recovery_Step0.ipynb)** from this repository, or use the Open in Colab button in the main README.
2. Open [Google Colab](https://colab.research.google.com/).
3. Choose **File → Open notebook → Upload** and select the `.ipynb` file. If Colab first shows its welcome dialog, use that dialog's **Upload** tab.
4. Give your notebook a team name and save a copy in your Google Drive.
5. Use a standard CPU runtime. No GPU or paid runtime is needed.

The notebook already contains the results of a local execution so you can inspect the finished charts. Run it yourself in Colab to create the files in your own workspace. Local execution does not mean the notebook has already run in your Google account.

## 2 Load the small BLS support ZIP

1. Download **[Step0_Colab_Support.zip](../downloads/Step0_Colab_Support.zip)** from this repository.
2. In Colab, open the **Files** panel on the left.
3. Upload this ZIP to the top-level runtime folder, `/content`. Leave it zipped.
4. The first code cell loads the BLS files from it automatically.

This ZIP contains the original BLS files used in the report, their metadata, and the input manifest. It is about 3 MB. BLS revises its live data; this copy lets us repeat the report's results. It was retrieved November 2, 2026, and is deliberately a fixed snapshot, not a claim to contain the newest release.

The setup cell preserves existing files. If your `raw` folder already contains a different BLS version, move those BLS files into a separate backup folder before rerunning setup with the support ZIP.

## 3 Choose how to supply HPS

**Easiest first run:** leave `USE_DRIVE = False`. The notebook downloads the nine original HPS archives directly from Census. Allow about 660 MB of downloads and several minutes of processing.

**Reuse files you already have:** keep the nine original Census CSV ZIPs intact. Do not rename them. You can either upload them into `/content/COVID_Step0/raw` after the setup cell creates that folder, or use Drive:

1. Make a Drive folder called `COVID_Step0`.
2. Inside it, make a folder called `raw`.
3. Place the nine original HPS ZIPs in `raw`.
4. Change `USE_DRIVE = True` in the notebook's first code cell.
5. Leave `DRIVE_PROJECT_FOLDER = "/content/drive/MyDrive/COVID_Step0"`, or change it to match your folder.
6. Run the cell and complete Google's Drive connection prompt.

The notebook checks existing files and downloads only missing ones. You need the original public-use ZIPs, which include the respondent CSVs and the matching person replicate weights. A single HPS cycle or an aggregate Census table is not enough for the full notebook.

## 4 Run the notebook in order

Use each code cell's ▶ button. Read the explanation above the cell first. You can also use **Runtime → Run all** once you understand the configuration. Do not run the chart cells before the data cells.

| Notebook section | What you do | What to look for |
|---|---|---|
| 1 Workspace | Choose runtime/Drive folder | Correct raw and results folders printed |
| 2 Variables | Read the code definitions | Understand SPN4 → EXPNS_DIF and adult weights |
| 3 Inputs | Run the download/fingerprint check | All 16 files present; fingerprints match |
| 4–5 Cleaning and weights | Read the rules, then run the definitions | Invalid answers excluded per outcome; no blanket deletion |
| 6 HPS | Run the main survey-processing cell | 610,755 responses, 80 replicates per cycle, 20 passing checks |
| 7 BLS | Run state/month/year preparation | 7,344 monthly rows and 306 annual rows |
| 8 Join | Run time alignment and join | 459 joined rows; zero unmatched left and right |
| 9 Evidence | Read the missingness and cleaning logs | Issues have actual affected-row counts |
| 10 Charts | Run all six chart cells | Titles, units, sources, and data-derived captions |
| 11 Drill-down | Inspect age groups nationally and in New York | Small groups are flagged/hidden, not replaced with zero |
| 12–13 Export | Run the export cell and download the ZIP | HTML briefing, charts, aggregate data, logs, provenance |

The main processing cell takes the longest. Wait for it to finish. A traceback means a check failed: read the last error and investigate rather than removing the check. Raw row counts, overlapping aggregate views, and joined rows are different quantities.

## 5 Review the 20-row comparison

The code selects 20 random records from the full HPS pool using a fixed seed. It rereads their original source rows and compares them with the processed values. The public `spotcheck_20_summary.csv` reports pass/fail results without respondent details.

Open **private_checks/spotcheck_20_raw_vs_processed.csv** in your own project folder. Use the notebook's variable table to check the original codes and their cleaned meanings. Have a teammate review the cases and record their initials, date, and any discrepancies in your private copy. The file starts with **Pending team review**; the notebook does not claim that a human has already checked it.

Keep that detailed table private. The downloadable briefing ZIP excludes it and all raw microdata.

## 6 Understand the six charts

1. **Sample overview:** respondent counts across the nine HPS cycles. This describes the survey sample, not population change.
2. **Time trend:** monthly seasonally adjusted unemployment rates in California, New York, and Texas, 2019–2024.
3. **Group comparison:** weighted financial hardship by work status within household income bands.
4. **Social outcomes:** frequent loneliness and anxiety symptoms within the two hardship groups.
5. **Joined comparison:** state hardship versus aligned BLS unemployment, with a descriptive rank correlation and an alignment sensitivity check.
6. **Distribution:** changes in annual state unemployment rates from 2019 to 2024.

HPS charts use valid adult responses, person weights, and 90% sampling intervals where applicable. Intervals do not remove nonresponse bias or establish causality. Differences have not been declared statistically significant by comparing whether intervals overlap.

## 7 Try another cycle or state

In the first code cell, edit:

```python
FOCUS_CYCLE = 9
FOCUS_STATE = "36"
TIMELINE_STATES = ["06", "36", "48"]
```

`36` is New York, `06` is California, and `48` is Texas. FIPS codes must stay text with two digits. After changing a setting, rerun the first code cell and all chart, drill-down, and export cells. Use **Run all** if unsure. The default briefing uses Cycle 9; the title and captions identify the actual collection dates.

Do not calculate the hardship percentage within a group already defined as having hardship and treat its 100% as a discovery. Similarly, avoid the support outcome within groups defined by that same support outcome. Those rows exist for other outcome comparisons.

## 8 Save your outputs

Download **COVID_Step0_Briefing_Pack.zip** from the project folder. Extract it and open **briefing_pack.html** in a browser. All six images are embedded, so the briefing can be shared as a single HTML file. Save the notebook too using **File → Download → Download .ipynb**.

Runtime-only files disappear when Colab resets. A Drive-based project persists in Drive. Review your own saved outputs before submitting.

## 9 Divide the team review

- One teammate reviews source versions, raw counts, and join checks.
- One reviews missingness, weights, reliability rules, and the private 20-case comparison.
- One reviews chart labels, captions, and the strength of the conclusions.
- A fourth teammate can assemble the stakeholder briefing and record the next round's questions. With three people, combine the last two roles.

We can now describe patterns and ask stakeholders what decisions they need to make. We cannot claim that unemployment caused loneliness, that the same people recovered over time, or that these measures provide a clinical diagnosis.

## If something fails

- **Fingerprint mismatch:** use the supplied BLS support ZIP for the report's exact snapshot. If you intentionally accept a revised BLS release, preserve it separately, review the revision and set `ALLOW_REVISED_BLS = True`. HPS changes still stop for review.
- **BLS download blocked:** upload the support ZIP into `/content` and rerun setup. No API key is needed.
- **HPS download interrupted:** rerun the input cell. Completed inputs are reused; partial downloads are not treated as complete files.
- **Missing archive or weight file:** use the original Census CSV ZIP for each cycle, not a manually assembled CSV or a published aggregate table.
- **Wrong folder:** use the raw-folder path printed by the first code cell. Drive and runtime storage are different places.
- **A plot has missing values:** inspect the suppression flags and group sample sizes. Missing and suppressed values are not zero.

## What was verified

See **[LOCAL_VALIDATION.md](LOCAL_VALIDATION.md)** in this folder for the actual local run results. The notebook is built for Colab and was executed locally against the audited original files. Execution in your Google account and manual team review remain your next steps.
