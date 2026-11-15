# NetCheck Lite — Free DNS and Single-Port TCP Checker

Small Python 3.9+ CLI to resolve a domain name or IP address and, optionally, connect to one selected TCP port. Standard library only.

## Run
From this folder:

    python3 netcheck_lite.py localhost
    python3 netcheck_lite.py localhost --port 443 --timeout 3

The first example checks DNS only. The second attempts one TCP handshake. A successful connection does not prove an application is healthy. Use on networks you own or have permission to assess.

## Exit codes
- 0: DNS resolved and optional connection succeeded
- 1: requested TCP connection failed
- 2: invalid input or DNS resolution failed

Run tests: python3 -m unittest discover -s tests -v

Optional [NetCheck — $12](https://zeftawy.gumroad.com/l/idlle?utm_source=github&utm_medium=repo_readme&utm_campaign=free_tools) adds selected multiple ports and structured timing/JSON output. This free tool remains fully usable.
