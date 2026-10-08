from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRAIN = (REPO / ".github" / "workflows" / "release-train.yml").read_text(encoding="utf-8")
CONFIG = json.loads((REPO / "release-please-config.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((REPO / ".release-please-manifest.json").read_text(encoding="utf-8"))


def _assert_actions_are_pinned(workflow: str) -> None:
    for line in workflow.splitlines():
        stripped = line.strip()
        if not stripped.startswith("uses:"):
            continue
        spec = stripped.split("uses:", 1)[1].strip()
        if spec.startswith("./"):
            continue
        name, _, ref = spec.partition("@")
        sha = ref.split()[0]
        assert name and len(sha) == 40, spec
        assert all(ch in "0123456789abcdef" for ch in sha), spec


def test_release_train_versions_template_without_pypi() -> None:
    package = CONFIG["packages"]["."]
    assert "branches:" in TRAIN and "- main" in TRAIN
    assert "googleapis/release-please-action@" in TRAIN
    assert "actions/create-github-app-token@" in TRAIN
    assert "repositories: mint-integration-template" in TRAIN
    assert "permission-contents: write" in TRAIN
    assert "permission-pull-requests: write" in TRAIN
    assert "permission-issues:" not in TRAIN
    assert package["release-type"] == "simple"
    assert package["package-name"] == "mint-integration-template"
    assert package["versioning-strategy"] == "prerelease"
    assert package["prerelease"] is True
    assert package["prerelease-type"] == "alpha"
    assert package["include-v-in-tag"] is True
    assert package["include-component-in-tag"] is False
    assert package["skip-labeling"] is True
    assert set(MANIFEST) == {"."}
    assert re.fullmatch(r"0\.\d+\.\d+-alpha\.\d+", MANIFEST["."])
    assert not (REPO / ".github" / "workflows" / "release.yml").exists()
    assert "pypa/gh-action-pypi-publish" not in TRAIN
    assert "PYPI_TOKEN" not in TRAIN
    assert "gh release create" not in TRAIN
    assert "git tag" not in TRAIN


def test_release_train_actions_are_commit_pinned() -> None:
    _assert_actions_are_pinned(TRAIN)


def test_instantiate_omits_release_please_files(tmp_path: Path) -> None:
    import subprocess
    import sys

    destination = tmp_path / "instantiated"
    completed = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "instantiate.py"), "--out", str(destination)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert not (destination / "release-please-config.json").exists()
    assert not (destination / ".release-please-manifest.json").exists()
    assert not (destination / ".github" / "workflows" / "release-train.yml").exists()
    assert not (destination / "tests" / "test_release_train.py").exists()
    assert (destination / "mint-integration.json").exists()
    assert (destination / "scripts" / "run_conformance.py").exists()
