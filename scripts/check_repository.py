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
require("All 19 code cells have execution counts", len(code_cells) == 19 and
        all(cell.get("execution_count") is not None for cell in code_cells))
outputs = [output for cell in code_cells for output in cell.get("outputs", [])]
require("Notebook has no error outputs", all(output["output_type"] != "error" for output in outputs))
require("Notebook has six saved inline figures", sum("image/png" in output.get("data", {}) for output in outputs) == 6)
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
require("All 216 recorded notebook checks passed", len(validation) == 216 and
        all(row["passed"].lower() == "true" for row in validation))
require("208 recorded cleaning decisions", len(rows("audit/step0/cleaning_decisions.csv")) == 208)
require("Six chart files", len(list((ROOT / "reports/step0/charts").glob("*.png"))) == 6)
require("Briefing embeds all six figures", (ROOT / "reports/step0/briefing_pack.html").read_text(encoding="utf-8").count("data:image/png;base64,") == 6)

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
