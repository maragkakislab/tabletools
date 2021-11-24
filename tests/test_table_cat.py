import unittest

from tabletools import table_cat


class TestTableCat(unittest.TestCase):
    def test_parser(self):
        parser = table_cat.parse_args(['foo', '-z'])
        self.assertEqual(parser.tables, ['foo'])
        self.assertTrue(parser.gunzip)

        parser = table_cat.parse_args(['foo', 'bar', '-z'])
        self.assertEqual(parser.tables, ['foo', 'bar'])
        self.assertTrue(parser.gunzip)

        parser = table_cat.parse_args(['foo', 'bar'])
        self.assertEqual(parser.tables, ['foo', 'bar'])
        self.assertFalse(parser.gunzip)


if __name__ == '__main__':
    unittest.main()
