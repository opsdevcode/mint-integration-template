# mint-integration-template

Template for a Mint integration. Replacement markers:

- `__MINT_INTEGRATION_IDENTITY__`
- `__MINT_INTEGRATION_NAMESPACE__`
- `__MINT_INTEGRATION_NAME__`
- `__MINT_INTEGRATION_VERSION__`
- `__MINT_INTEGRATION_CAPABILITY__`
- `__MINT_INTEGRATION_TARGET_KIND__`
- `__MINT_INTEGRATION_EXECUTABLE__`

```bash
python scripts/instantiate.py --out /tmp/my-mint-integration
python /tmp/my-mint-integration/scripts/run_conformance.py
```

CI instantiates the local.sandbox defaults and requires conformance
(`execute` refused). Do not publish this template as a PyPI package.
Release Please owns prerelease tags for this repository. Instantiation
omits the Release Please train. `mint apply` is not part of Mint.

## GitHub Release install and verify

Instantiated Python integrations are GitHub-first. There is no
integration PyPI and no `latest` tag. Download the prerelease wheel and
`SHA256SUMS`, check the digest, then install the local file:

```bash
curl -fsSL -O https://github.com/opsdevcode/mint-integration-local/releases/download/v0.2.0-alpha.1/SHA256SUMS
curl -fsSL -O https://github.com/opsdevcode/mint-integration-local/releases/download/v0.2.0-alpha.1/mint_integration_local-0.2.0a1-py3-none-any.whl
shasum -a 256 -c SHA256SUMS
pip install ./mint_integration_local-0.2.0a1-py3-none-any.whl
```

Recorded wheel digest:
`sha256:591e1b3ebdd7e4f9373996e0cdeafa62d8fea39d2640ded8270ff2e59c68094d`.
The GitHub integration sibling uses
`sha256:3c864b4f5e7298a0a2f52d0680cb5c3eb8ea57a8195e7d9ba628fe3b7b6e60da`.
Pin a tree with `mint integrations add --project DIR --local mint-integration.json`.
`add` does not pip or execute.
GitHub Releases are canonical (`opsdevcode.release/v0`). PyPI publication stays deferred.
