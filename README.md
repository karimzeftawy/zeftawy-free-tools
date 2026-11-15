# Free Python Tools — CleanCSV, TLS Expiry & NetCheck

Three small, fully free, open-source Python CLI utilities. The **complete free source** is right here in GitHub; downloading from Gumroad or buying anything is not required. Run locally with Python 3.9+ and no external Python dependencies.

## Three free tools

| Tool | Purpose | Source | Optional free Gumroad ZIP | Optional paid upgrade |
|---|---|---|---|---|
| CleanCSV Lite | Trim CSV whitespace, remove blank rows | [Source](cleancsv-lite/) | [Download free](https://zeftawy.gumroad.com/l/rwsbgq?utm_source=github&utm_medium=repository&utm_campaign=free_tools) | [CleanCSV Pro — $8](https://zeftawy.gumroad.com/l/jnqegk?utm_source=github&utm_medium=repository&utm_campaign=free_tools) |
| TLS Expiry Lite | Check verified TLS certificate expiry or offline demo | [Source](tls-expiry-lite/) | [Download free](https://zeftawy.gumroad.com/l/vuiwlv?utm_source=github&utm_medium=repository&utm_campaign=free_tools) | [CertWatch — $15](https://zeftawy.gumroad.com/l/wjdwi?utm_source=github&utm_medium=repository&utm_campaign=free_tools) |
| NetCheck Lite | DNS lookup and optional single-port TCP check | [Source](netcheck-lite/) | [Download free](https://zeftawy.gumroad.com/l/tkdxcl?utm_source=github&utm_medium=repository&utm_campaign=free_tools) | [NetCheck — $12](https://zeftawy.gumroad.com/l/idlle?utm_source=github&utm_medium=repository&utm_campaign=free_tools) |

## Quick start

Run from repository root:

    python3 cleancsv-lite/cleancsv_lite.py cleancsv-lite/samples/messy.csv cleaned.csv
    python3 tls-expiry-lite/tls_expiry_lite.py --sample tls-expiry-lite/samples/example_certificate.json
    python3 netcheck-lite/netcheck_lite.py localhost

For network targets, use only systems you own or are authorized to assess. Verified TLS checks do not bypass certificate checks and may error for untrusted/expired certificates. The synthetic TLS sample is clearly NOT a real website check.

## Run all tests

    (cd cleancsv-lite && python3 -m unittest discover -s tests -v)
    (cd tls-expiry-lite && python3 -m unittest discover -s tests -v)
    (cd netcheck-lite && python3 -m unittest discover -s tests -v)

Continuous integration runs the tests on pushes and pull requests.

## Further tools (optional)

[Complete Developer Toolkit — 10 utilities and templates for $60](https://zeftawy.gumroad.com/l/npjmye?utm_source=github&utm_medium=repository&utm_campaign=free_tools). Buying is not required to use this repository.

**Scope:** Small educational and productivity utilities, not commercial-grade monitoring or security products. Report bugs through GitHub Issues and do not post secrets or personal logs.
