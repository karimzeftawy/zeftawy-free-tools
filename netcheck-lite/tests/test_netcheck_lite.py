import socket
import unittest
from unittest.mock import patch

from netcheck_lite import check_tcp, main, resolve_host


class NetCheckLiteTests(unittest.TestCase):
    def test_localhost_dns_resolution(self):
        addrs = resolve_host('localhost')
        self.assertTrue(len(addrs) >= 1)
        self.assertTrue(all(isinstance(x, str) for x in addrs))

    def test_reject_whitespace_hostname(self):
        with self.assertRaises(ValueError):
            resolve_host('some host')

    def test_good_tcp_connection_to_local_listener(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(('127.0.0.1',0))
            listener.listen(1)
            good, msg = check_tcp('127.0.0.1',listener.getsockname()[1],1)
        self.assertTrue(good)
        self.assertIn('succeeded',msg)

    def test_bad_tcp_connection(self):
        with patch('netcheck_lite.socket.create_connection',side_effect=ConnectionRefusedError('refused')):
            good, msg = check_tcp('127.0.0.1',1234,0.5)
        self.assertFalse(good)
        self.assertIn('failed',msg)

    def test_validate_ports_and_timeouts(self):
        for port in [0,-1,65536]:
            with self.assertRaises(ValueError):
                check_tcp('localhost',port)
        with self.assertRaises(ValueError):
            check_tcp('localhost',443,0)

    def test_dns_only_cli(self):
        self.assertEqual(main(['localhost']),0)

    def test_invalid_port_cli(self):
        self.assertEqual(main(['localhost','--port','65536']),2)

    def test_dns_failure_cli(self):
        with patch('netcheck_lite.resolve_host',side_effect=socket.gaierror('host not found')):
            self.assertEqual(main(['not-real.invalid']),2)


if __name__ == '__main__':
    unittest.main()
