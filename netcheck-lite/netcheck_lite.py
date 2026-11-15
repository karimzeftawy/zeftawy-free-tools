#!/usr/bin/env python3
"""NetCheck Lite — basic DNS lookup and a single TCP port check."""
from __future__ import annotations

import argparse
import socket
import sys
from typing import List, Optional, Tuple


def resolve_host(host: str) -> List[str]:
    """Get unique IPv4/IPv6 addresses using the OS resolver."""
    if not host or any(char.isspace() for char in host):
        raise ValueError('Provide a hostname or IP address without spaces')
    results = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    return sorted({result[4][0] for result in results})


def check_tcp(host: str, port: int, timeout: float = 3.0) -> Tuple[bool, str]:
    """Connect to just one TCP port (not a port scanner)."""
    if not 1 <= port <= 65535:
        raise ValueError('Port must be between 1 and 65535')
    if not 0 < timeout <= 60:
        raise ValueError('Timeout must be > 0 and <= 60 seconds')
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, f'TCP {port}: connection succeeded'
    except OSError as exc:
        return False, f'TCP {port}: connection failed ({exc})'


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Free DNS and optional single TCP-port connectivity check')
    parser.add_argument('host', help='Domain name or IP address to check')
    parser.add_argument('--port', type=int, help='Optional single TCP port, e.g. 443')
    parser.add_argument('--timeout', type=float, default=3, help='Connection timeout in seconds (default: 3)')
    args = parser.parse_args(argv)
    try:
        if not 0 < args.timeout <= 60:
            raise ValueError('Timeout must be > 0 and <= 60 seconds')
        if args.port is not None and not 1 <= args.port <= 65535:
            raise ValueError('Port must be between 1 and 65535')
        addresses = resolve_host(args.host)
        print(f'Host: {args.host}')
        print(f'Addresses: {", ".join(addresses)}')
        if args.port is not None:
            good, message = check_tcp(args.host, args.port, args.timeout)
            print(message)
            if not good:
                return 1
        return 0
    except (socket.gaierror, OSError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
