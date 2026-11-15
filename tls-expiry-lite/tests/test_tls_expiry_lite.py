import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from tls_expiry_lite import get_certificate, get_expiry, main, print_result


class ExpiryLiteTests(unittest.TestCase):
    def setUp(self):
        self.fixed = datetime(2026, 11, 11, tzinfo=timezone.utc)

    def test_expiry_more_than_30_days(self):
        expiry, days = get_expiry({'notAfter':'Dec 31 00:00:00 2026 GMT'}, now=self.fixed)
        self.assertEqual(expiry.tzinfo, timezone.utc)
        self.assertEqual(days, 50)

    def test_expiring_soon_return_code(self):
        self.assertEqual(print_result('sample.local', {'notAfter':'Nov 30 00:00:00 2026 GMT'}, now=self.fixed), 1)

    def test_expired_return_code(self):
        self.assertEqual(print_result('sample.local', {'notAfter':'Nov 01 00:00:00 2026 GMT'}, now=self.fixed), 1)

    def test_missing_expiry_is_error(self):
        with self.assertRaises(ValueError):
            get_expiry({}, now=self.fixed)

    def test_now_must_be_aware(self):
        with self.assertRaises(ValueError):
            get_expiry({'notAfter':'Dec 31 00:00:00 2026 GMT'}, now=datetime(2026, 11, 11))

    @patch('tls_expiry_lite.socket.create_connection')
    @patch('tls_expiry_lite.ssl.create_default_context')
    def test_verified_tls_connection_and_sni(self, make_context, create_connection):
        raw = MagicMock()
        raw.__enter__.return_value = raw
        secure = MagicMock()
        secure.__enter__.return_value = secure
        secure.getpeercert.return_value = {'notAfter':'Dec 31 00:00:00 2026 GMT'}
        create_connection.return_value = raw
        make_context.return_value.wrap_socket.return_value = secure
        self.assertIn('notAfter', get_certificate('example.com', 443, 1.5))
        make_context.return_value.wrap_socket.assert_called_once_with(raw,server_hostname='example.com')
        create_connection.assert_called_once_with(('example.com',443),timeout=1.5)

    def test_rejects_invalid_port(self):
        with self.assertRaises(ValueError):
            get_certificate('example.com', 0)

    def test_cli_offline_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'cert.json'
            path.write_text(json.dumps({'notAfter':'Dec 31 23:59:59 2040 GMT'}))
            self.assertEqual(main(['--sample',str(path)]), 0)

    def test_sample_and_host_conflict(self):
        with self.assertRaises(SystemExit) as cm:
            main(['example.com','--sample','no.json'])
        self.assertEqual(cm.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
