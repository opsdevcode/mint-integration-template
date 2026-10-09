from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
CI = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")


def test_readme_documents_github_release_install_and_verify() -> None:
    assert "GitHub Release" in README or "GitHub prerelease" in README
    assert "SHA256SUMS" in README
    assert "shasum -a 256 -c SHA256SUMS" in README
    assert "pip install ./" in README
    assert "pypi.org/project/" not in README
    assert "latest" not in README or "no `latest`" in README or "not `latest`" in README
    assert "mint apply" in README
    assert "not a PyPI package" in README or "Do not publish this template as a PyPI package" in README


def test_ci_keeps_instantiate_and_forbids_pypi_publish() -> None:
    assert "scripts/instantiate.py" in CI
    assert "pypa/gh-action-pypi-publish" not in CI
    assert "PYPI_TOKEN" not in CI
