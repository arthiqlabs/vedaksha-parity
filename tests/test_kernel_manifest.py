"""verify_kernel against the real committed manifest and real local kernel
files — no mock. Skips cleanly if a kernel isn't present locally."""

import tempfile
from pathlib import Path

import pytest

from vedaksha_parity.kernel_manifest import verify_kernel
from vedaksha_parity.oracles.base import OracleUnsupported

_DE440 = Path("vendor/kernels/de440.bsp")
_INPOP = Path("vendor/kernels/inpop21a.bsp")


@pytest.mark.skipif(not _DE440.exists(), reason="vendor/kernels/de440.bsp not present locally")
def test_the_real_de440_file_verifies_clean():
    verify_kernel(_DE440)  # must not raise


@pytest.mark.skipif(not _INPOP.exists(), reason="vendor/kernels/inpop21a.bsp not present locally")
def test_the_real_inpop_file_verifies_clean():
    verify_kernel(_INPOP)  # must not raise


def test_an_unrecognized_filename_is_rejected():
    with tempfile.TemporaryDirectory() as d:
        unknown = Path(d) / "not-in-the-manifest.bsp"
        unknown.write_bytes(b"anything")
        with pytest.raises(OracleUnsupported, match="no entry"):
            verify_kernel(unknown)


def test_wrong_content_under_a_known_filename_is_rejected():
    # Same name as a real manifest entry, wrong bytes — must not pass on
    # filename alone.
    with tempfile.TemporaryDirectory() as d:
        fake = Path(d) / "de440.bsp"
        fake.write_bytes(b"not the real kernel")
        with pytest.raises(OracleUnsupported, match="size|SHA256"):
            verify_kernel(fake)
