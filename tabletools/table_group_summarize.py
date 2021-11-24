#!/usr/bin/env python

"""
Groups the entries of the input table file, essentially a csv file, and
summarizes the requested columns. The output summary columns are named by
concatenating the column name with the function name and an "_" in between
e.g. score_mean.
"""

import sys
import argparse
import pandas as pd


def get_input_file_object(filename):
    """
    Returns a file objects that reads from filename or from STDIN if filename
    is -
    """
    if filename == "-":
        return sys.stdin
    return open(filename, "r")


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-t", "--table", required=True, default='-',
                    help="Input csv file; STDIN if - (default: %(default)s)")
parser.add_argument("-g", "--groupby", required=True, nargs='+',
                    help="Name of column/s to group entries by")
parser.add_argument("-y", "--summarize", required=True, nargs='+',
                    help="Name of column to summarize")
parser.add_argument("-f", "--func", required=True, nargs='+',
                    help="Pandas function/s to summarize columns e.g. mean")
parser.add_argument("-s", "--sep", default='\t',
                    help="Column separator (default: <TAB>)")
args = parser.parse_args()

# Flatten the groupby and func options. They were lists of lists.
groupby = args.groupby
functions = args.func
summarize_cols = args.summarize

# Read the data.
table = get_input_file_object(args.table)
df = pd.read_csv(table, sep=args.sep)

summarize_dict = {}
for col in summarize_cols:
    summarize_dict[col] = functions

# Group and summarize the data.
grouped = df.groupby(groupby).agg(summarize_dict)
newcols = []
for col in summarize_cols:
    for f in functions:
        newcols.append(col+'_'+f)
grouped.columns = newcols
grouped = grouped.reset_index()

# Output grouped dataset.
grouped.to_csv(sys.stdout, sep=args.sep, index=False)
