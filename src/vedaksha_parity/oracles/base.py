"""The Oracle protocol every reference-engine adapter implements.

An oracle answers a case or raises OracleUnsupported. It must never return a
default value for something it cannot actually compute — a silent default is
indistinguishable from agreement, which is the worst failure mode for a
measuring instrument. See FIREWALL.md: an oracle is a sealed box that emits
numbers, never a source file to read.
"""

from __future__ import annotations

from typing import Any, Protocol


class OracleUnsupported(Exception):
    """Raised when an oracle cannot answer a case — a refusal, not a default."""


class Oracle(Protocol):
    NAME: str
    VERSION: str

    def settings(self) -> dict[str, Any]:
        """The configuration this oracle was pinned to, recorded in every run."""
        ...

    def answer(self, case: dict[str, Any]) -> dict[str, Any]:
        """Answer one case, or raise OracleUnsupported."""
        ...
