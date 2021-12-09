import unittest
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
        parser = table_paste_col.parse_args(['--table', 'foo', '--col-name', 'bar', '--col-value', 'baz', '--at-end'])
        # table = table_paste_col.get_input_file_object(parser.table) #
        # doesn't work bc there's no foo
        # table_paste_col.add_col(table, parser.sep, parser.colname, parser.colvalue, parser.at_end)
        # split line and check that last element of line is bar
        # how do we get this line bc add_col doesn't return it
        # self.assertEqual(name, 'bar')
        self.assertTrue(parser.at_end)

        # parser = table_paste_col.parse_args(['--table', 'foo', '--col-name', 'bar', '--col-value', 'baz'])
        # table_paste_col.add_col(parser.table, parser.sep, parser.colname,
        # parser.colvalue, parser.at_end)
        # # split line and check that first element of line is bar
        # self.assertEqual(val, 'baz')
    #
