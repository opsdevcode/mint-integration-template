"""Replace template markers. Never fetches or executes an integration."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

DEFAULTS = {
    "__MINT_INTEGRATION_IDENTITY__": "local.sandbox.ensure_marker",
    "__MINT_INTEGRATION_NAMESPACE__": "local.sandbox",
    "__MINT_INTEGRATION_NAME__": "ensure_marker",
    "__MINT_INTEGRATION_VERSION__": "0.1.0",
    "__MINT_INTEGRATION_CAPABILITY__": "local.sandbox.ensure_marker",
    "__MINT_INTEGRATION_TARGET_KIND__": "local.sandbox",
    "__MINT_INTEGRATION_EXECUTABLE__": "mint-integration-local",
}


def instantiate(source: Path, destination: Path, values: dict[str, str]) -> None:
    if destination.exists():
        raise SystemExit(f"refuse to overwrite {destination}")
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns(
            ".git",
            "release-please-config.json",
            ".release-please-manifest.json",
            "release-train.yml",
            "test_release_train.py",
        ),
    )
    for path in destination.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        updated = text
        for marker, value in values.items():
            updated = updated.replace(marker, value)
        if updated != text:
            path.write_text(updated, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Instantiate Mint integration template markers")
    parser.add_argument("--source", default=".", help="Template directory")
    parser.add_argument("--out", required=True, help="Destination directory")
    args = parser.parse_args()
    instantiate(Path(args.source).resolve(), Path(args.out).resolve(), dict(DEFAULTS))
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
