# Earlier Phase 1 acquisition and preparation

These are the original scripts behind the data-source research report. The executed notebook under `notebooks/` is the main Step 0 workflow and produces all six charts.

To reproduce the older broader audit, start in this folder using a separate Python environment and this folder's `requirements.txt`:

```bash
python -m pip install -r requirements.txt
python download_data.py --raw-dir raw --scope all
python reproduce_prepare.py --raw-dir raw --output-dir reproduced/data --audit-dir reproduced/audit
```

`--scope all` includes earlier HPS samples, the successor sample, and BRFSS audit inputs as well as the core sources. The downloader checks the original manifest's fingerprints and stops if a publisher changed a file. It does not silently accept revisions.

The broader script retains 2025 BLS data with incomplete-year flags and makes a small BRFSS parser sample. Those are not core Step 0 analytical inputs. `raw/` and `reproduced/` are ignored by Git; keep their respondent-level outputs private. Do not publish the BRFSS convenience microdata sample. The notebook provides the simpler two-source project workflow.
