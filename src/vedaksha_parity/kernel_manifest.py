"""Hash-verifies reference-engine kernel files against a committed
manifest before use. Filename is not identity: `de440.bsp` on disk could
be truncated, corrupted, or silently replaced with a different file that
still opens and still answers queries. See data/kernel-manifest.json.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from vedaksha_parity.oracles.base import OracleUnsupported

_MANIFEST_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "kernel-manifest.json"


def _load_manifest() -> dict[str, Any]:
    return json.loads(_MANIFEST_PATH.read_text())


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def verify_kernel(path: Path) -> None:
    """Raise OracleUnsupported unless `path`'s SHA256 matches the
    committed manifest entry for its filename. Called once, at oracle
    construction — never re-hashed per query, which would make every
    run pay for reading a 100+ MB file on every case."""
    manifest = _load_manifest()
    entry = manifest.get(path.name)
    if entry is None:
        raise OracleUnsupported(
            f"{path} has no entry in {_MANIFEST_PATH} — an unrecognized kernel "
            "file is not a verified one. Add it to the manifest deliberately, "
            "with its real SHA256, source, and retrieval date, or use the "
            "expected filename."
        )
    actual_size = path.stat().st_size
    if actual_size != entry["byte_length"]:
        raise OracleUnsupported(
            f"{path}: size {actual_size} bytes does not match the manifest's "
            f"{entry['byte_length']} bytes for {path.name} — refusing to trust "
            "an unverified file rather than silently reading it."
        )
    actual_sha256 = _sha256(path)
    if actual_sha256 != entry["sha256"]:
        raise OracleUnsupported(
            f"{path}: SHA256 {actual_sha256} does not match the manifest's "
            f"{entry['sha256']} for {path.name} — this is not the same file "
            "the manifest was written for, even though the name matches."
        )
