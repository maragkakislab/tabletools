import unittest
import pandas as pd
import pandas.testing as pd_testing

from tabletools import table_group_summarize

class TestTableCat(unittest.TestCase):
    def test_parser(self):
        parser = table_group_summarize.parse_args(['-t','foo', '-g','bar', '-y', 'stat', '-f','mean'])
        self.assertEqual(parser.table, 'foo')
        self.assertEqual(parser.groupby, ['bar'])
        self.assertEqual(parser.summarize, ['stat'])
        self.assertEqual(parser.func, ['mean'])

    def test_summarize_simple(self):
        df = pd.DataFrame(
            [[1,1],[1,2],[2,3],[2,4],[2,5],[3,6]],
            columns = ['id','column']
        )
        groupby = "id"
        functions = ['mean']
        summarize_cols = ['column']
        out = table_group_summarize.group_summarize(df, groupby, functions, summarize_cols)
        expected = pd.DataFrame(
            [[1,1.5],[2,4.0],[3,6.]],
            columns = ['id','column_mean']
        )
        pd_testing.assert_frame_equal(out, expected)

    def test_summarize_multifunc(self):
        df = pd.DataFrame(
            [[2,3],[2,4],[2,8]],
            columns = ['id','column']
        )
        groupby = "id"
        functions = ['mean','median']
        summarize_cols = ['column']
        out = table_group_summarize.group_summarize(df, groupby, functions, summarize_cols)
        expected = pd.DataFrame(
            [[2,5,4]],
            columns = ['id','column_mean','column_median']
        )
        pd_testing.assert_frame_equal(out, expected)

    def test_summarize_multicol(self):
        df = pd.DataFrame(
            [[1,1,2],[1,2,3],[2,3,4],[2,4,5],[2,5,6]],
            columns = ['id','column1','column2']
        )
        groupby = "id"
        functions = ['median']
        summarize_cols = ['column1','column2']
        out = table_group_summarize.group_summarize(df, groupby, functions, summarize_cols)
        expected = pd.DataFrame(
            [[1,1.5,2.5], [2,4,5]],
            columns = ['id','column1_median','column2_median']
        )
        pd_testing.assert_frame_equal(out, expected)

    def test_summarize_multimeancol(self):
        df = pd.DataFrame(
            [[1,1,2],[1,2,3],[2,0,1],[2,4,5],[2,5,6]],
            columns = ['id','column1','column2']
        )
        groupby = "id"
        functions = ['mean','median']
        summarize_cols = ['column1','column2']
        out = table_group_summarize.group_summarize(df, groupby, functions, summarize_cols)
        expected = pd.DataFrame(
            [[1,1.5,1.5,2.5,2.5], [2,3,4,4,5]],
            columns = ['id','column1_mean','column1_median','column2_mean','column2_median']
        )
        pd_testing.assert_frame_equal(out, expected)


if __name__ == '__main__':
    unittest.main()