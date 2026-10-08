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
