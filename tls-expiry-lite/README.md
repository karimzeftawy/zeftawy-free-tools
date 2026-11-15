# TLS Expiry Lite — Free Verified TLS Expiry CLI

Inspect a domain's TLS certificate expiration with Python's SSL library and **certificate + hostname verification enabled**. Useful for manual checks of systems you administer.

## Requirements
Python 3.9+. For live checks, internet access and a CA-trusted certificate.

## Run
From this folder:

    python3 tls_expiry_lite.py example.com
    python3 tls_expiry_lite.py example.com --port 443 --timeout 5
    python3 tls_expiry_lite.py --sample samples/example_certificate.json

The bundled example is synthetic offline metadata, NOT a real certificate check.

## Exit codes
- 0: more than 30 days remain
- 1: 30 days or fewer remain
- 2: connection, validation, or input error

An expired or untrusted certificate may fail verification before metadata is retrieved; the utility does not disable TLS validation. Not a persistent monitor or vulnerability scanner.

Run tests: python3 -m unittest discover -s tests -v

Optional [CertWatch — $15](https://zeftawy.gumroad.com/l/wjdwi?utm_source=github&utm_medium=repo_readme&utm_campaign=free_tools) adds certificate details, JSON output, and configurable thresholds. This free tool remains fully usable.
