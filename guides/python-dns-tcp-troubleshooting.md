# DNS resolution versus TCP connectivity: a practical Python checklist

A hostname resolving correctly does **not** mean the application behind it is available. These two network checks answer different questions and need to be interpreted separately.

## Question 1: Can the name resolve?

DNS maps domain names to one or more addresses. Python can use the operating system resolver:

```python
import socket

for item in socket.getaddrinfo("example.com", None, type=socket.SOCK_STREAM):
    print(item[4][0])
```

If this fails, investigate the hostname spelling, local resolver settings, DNS records, search domains, and network access to the configured DNS server.

If it succeeds, the host could still be offline, filtered, or listening on a different port.

## Question 2: Can a TCP handshake complete?

Use `socket.create_connection` with a bounded timeout:

```python
import socket

try:
    with socket.create_connection(("example.com", 443), timeout=3):
        print("TCP connection established")
except OSError as exc:
    print(f"TCP connection failed: {exc}")
```

A successful connection suggests that a TCP service accepted a connection at that moment. It does **not** prove TLS validation, HTTP health, authentication, or correct application responses.

## Interpreting common cases

| DNS | TCP | Possible explanation |
|---|---|---|
| Fails | Not attempted | Typo, resolver issue, or missing DNS record |
| Succeeds | Refused | Target reachable but no listener, or an active reject |
| Succeeds | Times out | Filtering, packet loss, routing issue, or unavailable host |
| Succeeds | Connects | A TCP listener is reachable; validate the actual protocol next |

A single hostname can resolve to multiple IP addresses and may vary by location, IPv4/IPv6, and time. A client connection might try more than one address.

## Safe diagnostic workflow

1. Confirm the exact hostname and intended port.
2. Check DNS resolution.
3. Attempt one authorized TCP connection with a timeout.
4. For HTTPS, verify TLS with hostname and CA validation.
5. Check an application-level health endpoint if you administer the service.
6. Record the time, error, and network environment so the result is reproducible.

Only test endpoints you own or have authorization to assess. This example does not teach broad port scanning.

## Free runnable code

[NetCheck Lite source and tests](../netcheck-lite/) provide DNS resolution and an optional single TCP port check on Python 3.9+.

For optional multiple selected ports and JSON/timing details, see [NetCheck — $12](https://zeftawy.gumroad.com/l/idlle?utm_source=github&utm_medium=guide&utm_campaign=dns_help).

The basic checker is completely free and open source.
