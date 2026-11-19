"""Check the committed notebook, aggregate data, source snapshot, and local links.

Uses Python's standard library; does not download respondent data or rerun analysis.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
checks = []


def require(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def rows(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


notebook = json.loads((ROOT / "notebooks/COVID_Recovery_Step0.ipynb").read_text(encoding="utf-8"))
require("Notebook uses format 4", notebook["nbformat"] == 4)
code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
require("All current code cells have execution counts", len(code_cells) >= 29 and
        all(cell.get("execution_count") is not None for cell in code_cells))
outputs = [output for cell in code_cells for output in cell.get("outputs", [])]
require("Notebook has no error outputs", all(output["output_type"] != "error" for output in outputs))
manifest_rows = rows("reports/step0/chart_captions.csv")
require("Notebook has every current saved inline figure", len(manifest_rows) == 23 and
        sum("image/png" in output.get("data", {}) for output in outputs) == len(manifest_rows))
for cell in code_cells:
    source = cell["source"]
    compile("".join(source) if isinstance(source, list) else source, "notebook cell", "exec")
require("Notebook code parses", True)

aggregate = rows("data/processed/hps_2024_aggregates.csv")
key_columns = ["state_fips", "cycle", "dimension", "group"]
require("8892 unique aggregate rows", len(aggregate) == 8892 and
        len({tuple(row[column] for column in key_columns) for row in aggregate}) == len(aggregate))
joined = rows("data/processed/joined_state_cycle_2024.csv")
require("459 unique state-cycle join rows", len(joined) == 459 and
        len({(row["state_fips"], row["cycle"]) for row in joined}) == 459)
require("51 two-digit jurisdiction keys", len({row["state_fips"] for row in joined}) == 51 and
        all(re.fullmatch(r"\d{2}", row["state_fips"]) for row in joined))
require("BLS monthly scope count", len(rows("data/processed/laus_state_month_2019_2024.csv")) == 7344)
require("BLS annual scope count", len(rows("data/processed/laus_state_annual_2019_2024.csv")) == 306)
require("HPS raw total", sum(int(row["raw_rows"]) for row in rows("audit/step0/hps_raw_row_counts.csv")) == 610755)
spotcheck = rows("audit/step0/spotcheck_20_summary.csv")
require("20 successful automated spot-checks", len(spotcheck) == 20 and
        all(row["all_passed"].lower() == "true" for row in spotcheck))
validation = rows("audit/step0/validation_checks.csv")
run_summary = json.loads((ROOT / "audit/step0/run_summary.json").read_text())
require("All recorded notebook checks passed", len(validation) == run_summary["validation_checks"] and len(validation) >= 216 and
        all(row["passed"].lower() == "true" for row in validation))
require("208 recorded cleaning decisions", len(rows("audit/step0/cleaning_decisions.csv")) == 208)
require("Every current chart file exists", len(list((ROOT / "reports/step0/charts").glob("*.png"))) == len(manifest_rows) and
        all((ROOT / "reports/step0/charts" / row["file"]).exists() for row in manifest_rows))
require("Briefing embeds every current figure", (ROOT / "reports/step0/briefing_pack.html").read_text(encoding="utf-8").count("data:image/png;base64,") == len(manifest_rows))
request_status = rows("personas/round1_request_status.csv")
require("17 Round 1 requests have explicit dispositions", len(request_status) == 17 and
        {row["id"] for row in request_status} == {str(i) for i in range(1,18)} and
        all(row["status"] in {"answered","partially answered","not answerable with this data","out of scope"} and row["reason"] for row in request_status))
recovery = rows("reports/round1_followup/state_recovery_table_with_flags.csv")
virginia = next(row for row in recovery if row["state_fips"] == "51")
require("Virginia's one-tenth boundary is correctly classified", virginia["rounding_band"] == "Within +/-0.1 pp" and
        virginia["published_rate_at_or_below_2019"].lower() == "false")
require("All 459 follow-up state cycles retained", len(rows("reports/round1_followup/state_hardship_by_cycle.csv")) == 459)
require("Seven follow-up charts include age reliability", len(rows("reports/round1_followup/chart_captions.csv")) == 7 and
        (ROOT/"reports/round1_followup/charts/23_reliability_heatmap_age.png").exists())

forbidden_fields = {"SCRAM", "SCRAMID", "TBIRTH_YEAR", "ABIRTH_YEAR", "SEQNO", "IDATE", "_PSU", "respondent_id", "raw_row_position"}
for path in ROOT.rglob("*.csv"):
    if ".git" in path.parts:
        continue
    with path.open(encoding="utf-8", newline="") as handle:
        fields = next(csv.reader(handle))
    require("No respondent fields: " + str(path.relative_to(ROOT)), not (set(fields) & forbidden_fields))
for path in ROOT.rglob("*"):
    if ".git" in path.parts:
        continue
    require("No raw/private folder: " + str(path.relative_to(ROOT)),
            not (set(path.relative_to(ROOT).parts) & {"raw", "private_checks"}))
    if path.is_file():
        require("Under GitHub file limit: " + str(path.relative_to(ROOT)), path.stat().st_size < 100 * 1024 * 1024)

manifest = {row["file"]: row for row in json.loads((ROOT / "audit/step0/input_manifest.json").read_text())}
with zipfile.ZipFile(ROOT / "downloads/Step0_Colab_Support.zip") as archive:
    inputs = [name for name in archive.namelist() if name.startswith("raw/")]
    require("Support ZIP has seven BLS files only", len(inputs) == 7 and all(Path(name).name.startswith("la.") for name in inputs))
    for name in inputs:
        require("BLS snapshot hash: " + name,
                hashlib.sha256(archive.read(name)).hexdigest() == manifest[Path(name).name]["sha256"])

for path in ROOT.rglob("*.md"):
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        target = target.strip().strip("<>").split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        require("Local link: " + str(path.relative_to(ROOT)) + " → " + target,
                (path.parent / unquote(target)).exists())

print(f"Passed {len(checks)} repository checks. Notebook outputs, data grains, privacy fields, BLS hashes, and local links verified.")
