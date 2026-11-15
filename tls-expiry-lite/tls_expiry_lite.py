#!/usr/bin/env python3
"""TLS Expiry Lite: check a *verified* server certificate's expiration date."""
from __future__ import annotations

import argparse
import json
import math
import socket
import ssl
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple


def get_certificate(host: str, port: int = 443, timeout: float = 5.0) -> Dict:
    """Use CA-chain and hostname validation. Does not disable TLS verification."""
    if not 1 <= port <= 65535:
        raise ValueError("Port must be 1..65535")
    if not 0 < timeout <= 60:
        raise ValueError("Timeout must be > 0 and <= 60 seconds")
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=timeout) as raw:
        with context.wrap_socket(raw, server_hostname=host) as secure:
            cert = secure.getpeercert()
    if not cert or not cert.get('notAfter'):
        raise ValueError("Verified certificate has no notAfter expiration value")
    return cert


def get_expiry(cert: Dict, now: Optional[datetime] = None) -> Tuple[datetime, int]:
    """Return UTC expiry and complete days until expiry, rounded up."""
    if 'notAfter' not in cert:
        raise ValueError("Certificate metadata has no notAfter expiration value")
    expiry = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert['notAfter']), timezone.utc)
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    remaining = math.ceil((expiry - now).total_seconds() / 86400)
    return expiry, remaining


def print_result(host: str, cert: Dict, now: Optional[datetime] = None) -> int:
    expiry, days = get_expiry(cert, now=now)
    if days <= 0:
        status, code = 'EXPIRED', 1
    elif days <= 30:
        status, code = 'EXPIRING SOON', 1
    else:
        status, code = 'VALID (more than 30 days remaining)', 0
    print(f'Host: {host}')
    print(f'Expires (UTC): {expiry:%Y-%m-%d %H:%M:%S}')
    print(f'Days remaining (rounded up): {days}')
    print(f'Status: {status}')
    return code


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Free verified TLS certificate expiry checker')
    parser.add_argument('host', nargs='?', help='Domain to check (example.com)')
    parser.add_argument('--port', type=int, default=443, help='TLS port (default: 443)')
    parser.add_argument('--timeout', type=float, default=5.0, help='TCP timeout in seconds (default: 5)')
    parser.add_argument('--sample', type=Path, help='Load an OFFLINE sample JSON certificate instead of connecting')
    args = parser.parse_args(argv)
    if not args.sample and not args.host:
        parser.error('Provide a domain or --sample path')
    if args.sample and args.host:
        parser.error('Specify either a domain or --sample, not both')
    try:
        if args.sample:
            data = json.loads(args.sample.read_text(encoding='utf-8'))
            if not isinstance(data, dict):
                raise ValueError('Sample JSON must be an object with notAfter')
            print('[OFFLINE SAMPLE — NOT A REAL DOMAIN CHECK]')
            return print_result('sample.local', data)
        cert = get_certificate(args.host, args.port, args.timeout)
        return print_result(args.host, cert)
    except (ValueError, TypeError, OSError, ssl.SSLError, json.JSONDecodeError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        print('This tool requires a trusted, valid TLS connection; it never disables verification.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
