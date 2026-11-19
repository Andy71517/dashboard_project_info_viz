"""Recover the audited BLS inputs without depending on BLS allowing cloud IPs.

The repository mirror contains the exact original BLS bytes, not new data.
Both the archive and each extracted member must match the audited fingerprints.
"""
from pathlib import Path
import hashlib
import urllib.request
from urllib.parse import urlsplit, urlunsplit
import zipfile
import io

BLS_SUPPORT_URL = "https://raw.githubusercontent.com/Andy71517/dashboard_project_info_viz/62153e402b92ea936d90a2243033ae892b88943a/downloads/Step0_Colab_Support.zip"
BLS_SUPPORT_SHA256 = "63380586805710db8ea40a60e806b1bb15c12c99414afe502ea0766efaa8d05c"


def official_bls_urls(url):
    """Try both official hosts regardless of which one the manifest lists."""
    parts = urlsplit(url)
    if parts.hostname not in {"download.bls.gov", "downloadt.bls.gov"}:
        return [url]
    alternate = "downloadt.bls.gov" if parts.hostname == "download.bls.gov" else "download.bls.gov"
    return [url, urlunsplit((parts.scheme, alternate, parts.path, parts.query, parts.fragment))]


def install_bls_snapshot(raw_dir, manifest, local_archives=(), cache_dir=None):
    """Install only missing BLS files; preserve existing inputs and never bypass hashes.

    Returns archive provenance and installed filenames. If every BLS input is
    already present, this does not access the network. Invalid archives or member
    fingerprints fail before writing any data. Existing files are subsequently
    checked by the notebook's normal input-verification loop.
    """
    raw_dir = Path(raw_dir)
    bls = {item["file"]: item for item in manifest if item["file"].startswith("la.")}
    missing = [name for name in bls if not (raw_dir / name).exists()]
    if not missing:
        return {"method": "existing files", "installed_files": []}
    candidates = [Path(path) for path in local_archives]
    cache = Path(cache_dir) / "Step0_Colab_Support.zip" if cache_dir is not None else None
    if cache is not None:
        candidates.append(cache)
    archive_path = next((path for path in candidates if path.is_file()), None)
    if archive_path is not None:
        payload = archive_path.read_bytes()
        archive_url = "local:" + archive_path.name
    else:
        request = urllib.request.Request(BLS_SUPPORT_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
        archive_url = BLS_SUPPORT_URL
    actual_archive_hash = hashlib.sha256(payload).hexdigest()
    if actual_archive_hash != BLS_SUPPORT_SHA256:
        raise ValueError("BLS support ZIP fingerprint mismatch. Preserve it and use the verified repository archive.")
    verified = {}
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for name, item in bls.items():
            # Construct fixed exact names, never trust archive paths for extraction.
            content = archive.read("raw/" + name)
            if hashlib.sha256(content).hexdigest() != item["sha256"]:
                raise ValueError("BLS archive member fingerprint mismatch: " + name)
            verified[name] = content
    if archive_path is None and cache is not None:
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(payload)
    raw_dir.mkdir(parents=True, exist_ok=True)
    for name in missing:
        target = raw_dir / name
        temporary = target.with_name(target.name + ".snapshot.part")
        temporary.write_bytes(verified[name])
        temporary.replace(target)
    return {"method": "audited BLS snapshot", "archive_url": archive_url,
            "archive_sha256": actual_archive_hash, "installed_files": missing}
