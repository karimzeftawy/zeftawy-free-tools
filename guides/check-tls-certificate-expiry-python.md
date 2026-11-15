# Check TLS certificate expiry in Python without disabling verification

Certificate expiry is easy to overlook until a production client refuses to connect. Here's a basic way to check the expiration date from a **verified** TLS connection using only Python's standard library.

## Why verification matters

Some online snippets disable validation with `CERT_NONE` or `check_hostname = False`. That can allow a man-in-the-middle to substitute an attacker-controlled certificate.

For a routine operational check, prefer Python's `ssl.create_default_context()`. It enables trusted CA-chain and hostname verification for client connections.

## 1. Connect securely

```python
import socket
import ssl

host = "example.com"
context = ssl.create_default_context()

with socket.create_connection((host, 443), timeout=5) as sock:
    with context.wrap_socket(sock, server_hostname=host) as tls_sock:
        cert = tls_sock.getpeercert()

print(cert.get("notAfter"))
```

The `server_hostname` argument supplies SNI and enables hostname verification. A trusted connection returns a certificate dictionary with fields such as `notAfter`.

## 2. Convert expiry to a timezone-aware value

The `notAfter` string normally resembles `Dec 31 23:59:59 2026 GMT`.

```python
from datetime import datetime, timezone
import ssl

expiry_epoch = ssl.cert_time_to_seconds(cert["notAfter"])
expiry_utc = datetime.fromtimestamp(expiry_epoch, timezone.utc)
remaining_days = (expiry_utc - datetime.now(timezone.utc)).total_seconds() / 86400

print(f"Expiry (UTC): {expiry_utc.isoformat()}")
print(f"Days remaining: {remaining_days:.1f}")
```

Use timezone-aware values for date arithmetic and think carefully about rounding rules around the final day.

## 3. Beware of an important edge case

If the target certificate has already expired, is self-signed without a trusted root, or has the wrong hostname, **the verified TLS handshake usually fails** before `getpeercert()` can return normal certificate metadata. This is the correct secure behavior.

Don't interpret a TLS verification failure as "more than 30 days remain." Treat it as a separate operational alert. If you need to inspect an untrusted certificate, use a separately designed diagnostic workflow with clearly labeled unverified data, not a silent production bypass.

## 4. Manual checks aren't monitoring

This example makes a single connection. It does not schedule checks, send notifications, track a fleet of hosts, or guarantee that every edge and load balancer serves the same certificate. Validate real services over their actual DNS names and ports.

## Try the free project

[TLS Expiry Lite source, README, offline sample, and tests](../tls-expiry-lite/) offers a verified CLI check and a clearly marked synthetic offline demonstration.

For optional issuer, SAN, JSON output, and warning configuration, see [CertWatch — $15](https://zeftawy.gumroad.com/l/wjdwi?utm_source=github&utm_medium=guide&utm_campaign=tls_help).

The free tool is fully usable without purchasing anything.
