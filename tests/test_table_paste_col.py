import unittest
import pandas as pd
from io import StringIO
from tabletools import table_paste_col

class TestTablePasteCol(unittest.TestCase):
    def test_parser(self):
        parser = table_paste_col.parse_args(['--table', 'foo', '--col-name', 'bar', '--col-value', 'baz', '--at-end'])
        self.assertEqual(parser.table, 'foo')
        self.assertEqual(parser.col_name, 'bar')
        self.assertEqual(parser.col_value, 'baz')
        self.assertTrue(parser.at_end)
        
        parser = table_paste_col.parse_args(['--table', 'foo', '--col-name', 'bar', '--col-value', 'baz'])
        self.assertEqual(parser.table, 'foo')
        self.assertEqual(parser.col_name, 'bar')
        self.assertEqual(parser.col_value, 'baz')
        self.assertFalse(parser.at_end)
        
    def test_add_col(self):
        parser = table_paste_col.parse_args(['--table', 'file1', '--col-name', 'foo', '--col-value', 'bar', '--at-end'])
        file1 = StringIO("A\tB\tC\nD\tE\tF\nG\tH\tI")
        out = table_paste_col.add_col(file1, parser.separator, parser.col_name, parser.col_value, parser.at_end)
        expected = StringIO("A\tB\tC\tfoo\nD\tE\tF\tbar\nG\tH\tI\tbar")
        self.assertEqual(out, expected)
        # expected = pd.DataFrame([['D', 'E', 'F', 'bar'], ['G', 'H', 'I', 'bar']], columns=['A', 'B', 'C', 'foo'])#, sep=parser.separator)
        # pd.testing.assert_frame_equal(df, expected)

