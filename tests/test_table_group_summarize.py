import unittest
import pandas as pd

from tabletools import table_group_summarize

class TestTableCat(unittest.TestCase):
    def test_parser(self):
        parser = table_group_summarize.parse_args(['-t','foo', '-g','bar', '-y', 'stat', '-f','mean'])
        self.assertEqual(parser.table, 'foo')
        self.assertEqual(parser.groupby, ['bar'])
        self.assertEqual(parser.summarize, ['stat'])
        self.assertEqual(parser.func, ['mean'])

    def test_summarize(self):
        df = pd.DataFrame(
            [[1,1],[1,2],[2,3],[2,4],[2,5],[3,6]],
            columns = ['id','column']
        )
        groupby = "id"
        functions = ['mean']
        summarize_cols = ['column']
        out = table_group_summarize.group_summarize(df, groupby, functions, summarize_cols)
        self.assertListEqual(list(out.columns),['id','column_mean'])
        
        self.assertEqual(out.at[0,'column_mean'],1.5)
        self.assertEqual(out.at[1,'column_mean'],4.0)
        self.assertEqual(out.at[2,'column_mean'],6)



if __name__ == '__main__':
    unittest.main()