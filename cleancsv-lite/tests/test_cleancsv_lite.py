import csv
import tempfile
import unittest
from pathlib import Path

from cleancsv_lite import clean_csv, main


class CleanCsvLiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / "messy.csv"
        self.dest = self.root / "clean.csv"

    def test_trims_and_skips_blank_rows_and_preserves_duplicates(self):
        self.src.write_text('Name, City\n Alice , Cairo \n ,  \n Alice , Cairo \n', encoding='utf-8')
        self.assertEqual(clean_csv(self.src, self.dest), (3, 1))
        with self.dest.open(newline='', encoding='utf-8') as fh:
            rows = list(csv.reader(fh))
        self.assertEqual(rows, [['Name','City'],['Alice','Cairo'],['Alice','Cairo']])

    def test_handles_utf8_bom_and_comma_inside_quotes(self):
        self.src.write_bytes(b'\xef\xbb\xbf"Product","Details"\n" Widget ","one, two"\n')
        self.assertEqual(clean_csv(self.src, self.dest), (2, 0))
        self.assertEqual(self.dest.read_text(encoding='utf-8'), 'Product,Details\nWidget,"one, two"\n')

    def test_never_modifies_source_in_place(self):
        self.src.write_text('ok\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            clean_csv(self.src, self.src)
        self.assertEqual(self.src.read_text(), 'ok\n')

    def test_existing_output_not_overwritten(self):
        self.src.write_text('ok\n', encoding='utf-8')
        self.dest.write_text('keep\n', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            clean_csv(self.src, self.dest)
        self.assertEqual(self.dest.read_text(), 'keep\n')

    def test_invalid_unicode_removes_partial_output(self):
        self.src.write_bytes(b'first\n\xff\n')
        with self.assertRaises(UnicodeError):
            clean_csv(self.src, self.dest)
        self.assertFalse(self.dest.exists())

    def test_cli_exit_code(self):
        self.src.write_text('a\n', encoding='utf-8')
        self.assertEqual(main([str(self.src), str(self.dest)]), 0)
        self.assertEqual(main([str(self.src), str(self.dest)]), 2)


if __name__ == '__main__':
    unittest.main()
