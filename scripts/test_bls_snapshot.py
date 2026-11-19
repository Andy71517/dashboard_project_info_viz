"""Regression tests for BLS 403 recovery; no live network required."""
from pathlib import Path
import hashlib
import io
import json
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bls_snapshot as recovery

MANIFEST = json.loads((ROOT / "audit/step0/input_manifest.json").read_text())
BLS = [item for item in MANIFEST if item["file"].startswith("la.")]
BUNDLE = (ROOT / "downloads/Step0_Colab_Support.zip").read_bytes()
NOTEBOOK = json.loads((ROOT / "notebooks/COVID_Recovery_Step0.ipynb").read_text(encoding="utf8"))
CELL = "".join(NOTEBOOK["cells"][7]["source"])


class SnapshotRecoveryTests(unittest.TestCase):
    def assert_files(self, raw):
        for item in BLS:
            self.assertEqual(hashlib.sha256((raw / item["file"]).read_bytes()).hexdigest(), item["sha256"])

    def test_both_official_hosts_in_either_direction(self):
        for host in ["download.bls.gov", "downloadt.bls.gov"]:
            urls = recovery.official_bls_urls(f"https://{host}/pub/time.series/la/la.txt")
            self.assertEqual(len(urls), 2)
            self.assertTrue(any("//download.bls.gov/" in u for u in urls))
            self.assertTrue(any("//downloadt.bls.gov/" in u for u in urls))

    def test_census_url_unchanged(self):
        url = "https://www2.census.gov/example.zip"
        self.assertEqual(recovery.official_bls_urls(url), [url])

    def test_uploaded_bundle_needs_no_network(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            archive = base / "upload.zip"
            archive.write_bytes(BUNDLE)
            with patch("urllib.request.urlopen", side_effect=AssertionError("Network used")):
                status = recovery.install_bls_snapshot(base / "raw", MANIFEST, [archive])
            self.assertEqual(len(status["installed_files"]), 7)
            self.assert_files(base / "raw")

    def test_missing_files_recovered_in_actual_notebook_cell_when_bls_is_403(self):
        calls = []
        def open_url(request, **kwargs):
            calls.append(request.full_url)
            if request.full_url == recovery.BLS_SUPPORT_URL:
                return io.BytesIO(BUNDLE)
            raise HTTPError(request.full_url, 403, "Forbidden", {}, None)
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            raw, results = base / "raw", base / "results"
            raw.mkdir(); results.mkdir()
            namespace = dict(BASE=base, RAW=raw, RESULTS=results, INPUT_MANIFEST=BLS,
                             ALLOW_REVISED_BLS=False, pd=Mock(), datetime=datetime, timezone=timezone,
                             print=Mock())
            with patch("urllib.request.urlopen", side_effect=open_url):
                exec(compile(CELL, "actual notebook acquisition cell", "exec"), namespace)
            self.assert_files(raw)
            self.assertEqual(calls, [recovery.BLS_SUPPORT_URL])
            self.assertTrue(all(row["matches_report_snapshot"] for row in namespace["acquisition"]))
            self.assertTrue(all(row["method"] == "audited BLS snapshot" for row in namespace["acquisition"]))

    def test_corrupt_bundle_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            archive = base / "bad.zip"; archive.write_bytes(b"not the verified archive")
            with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
                recovery.install_bls_snapshot(base / "raw", MANIFEST, [archive])
            self.assertFalse((base / "raw").exists())

    def test_member_fingerprint_checked_in_addition_to_bundle(self):
        manifest = [dict(item) for item in BLS]
        manifest[0]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            archive = base / "upload.zip"; archive.write_bytes(BUNDLE)
            with self.assertRaisesRegex(ValueError, "member fingerprint mismatch"):
                recovery.install_bls_snapshot(base / "raw", manifest, [archive])
            self.assertFalse((base / "raw").exists())

    def test_existing_file_preserved_for_normal_source_change_check(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder); raw = base / "raw"; raw.mkdir()
            (raw / "la.txt").write_bytes(b"existing version")
            archive = base / "upload.zip"; archive.write_bytes(BUNDLE)
            recovery.install_bls_snapshot(raw, MANIFEST, [archive])
            self.assertEqual((raw / "la.txt").read_bytes(), b"existing version")
            with patch("urllib.request.urlopen", side_effect=AssertionError("Network used")):
                self.assertEqual(recovery.install_bls_snapshot(raw, MANIFEST)["installed_files"], [])

    def test_fully_blocked_network_reports_both_hosts_and_manual_recovery(self):
        calls = []
        def blocked(request, **kwargs):
            calls.append(request.full_url)
            raise HTTPError(request.full_url, 403, "Forbidden", {}, None)
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder); raw = base / "raw"; raw.mkdir()
            results = base / "results"; results.mkdir()
            la_txt = [item for item in BLS if item["file"] == "la.txt"]
            namespace = dict(BASE=base, RAW=raw, RESULTS=results, INPUT_MANIFEST=la_txt,
                             ALLOW_REVISED_BLS=False, pd=Mock(), datetime=datetime, timezone=timezone, print=Mock())
            with patch("urllib.request.urlopen", side_effect=blocked):
                with self.assertRaisesRegex(RuntimeError, "Upload Step0_Colab_Support.zip into /content") as error:
                    exec(compile(CELL, "actual notebook acquisition cell", "exec"), namespace)
            self.assertIn("https://download.bls.gov/", str(error.exception))
            self.assertIn("https://downloadt.bls.gov/", str(error.exception))
            self.assertEqual(len(calls), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
