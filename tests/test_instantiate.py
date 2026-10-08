from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_markers_are_present() -> None:
    text = (ROOT / "implementation" / "reference_server.py").read_text(encoding="utf-8")
    assert "__MINT_INTEGRATION_IDENTITY__" in text
    assert "mint apply" not in text
