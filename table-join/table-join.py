#!/usr/bin/env python

"""
Join the columns of two tables based on given key columns, using
(pandas dataframe.merge option). Assumes that the input file has a
header line with column names.
"""

import argparse
import sys
import pandas as pd

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-t","--table1",
                    help = "Input first table file; reads from STDIN if '-'")
parser.add_argument("-g","--table2",
                    help = "Input second table file; reads from STDIN if '-'")
parser.add_argument("-c","--key1", nargs='+',
                    help = "Name(s) of column (headers) first table")
parser.add_argument("-d","--key2", nargs='+',
                    help = "Name(s) of column (headers) second table")
parser.add_argument("-x","--suffix1", default="x",
                    help = "Suffix to add to overlapping column names,(default: %(default)s)")
parser.add_argument("-y","--suffix2", default="y",
                    help = "Suffix to add to overlapping column names,(default: %(default)s)")
parser.add_argument("-s", "--delim", default="\t",
                    help="Delimiter to separate the columns of the output file, default : <TAB>")
parser.add_argument("-k","--how", default= "inner",
                    help = "How to merge ‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’,(default: %(default)s)")
args = parser.parse_args()

def get_filehandle(filename):
    """ Returns a filehandle """
    if filename == "-":
        return sys.stdin
    return open(filename, "r")

#Condition for NOT taking both input files (file1 & file2) via stdin
if args.table1 == "-" and  args.table2 == "-":
    print("Error: can't provide stdin twice as input", file=sys.stderr)
    sys.exit(1)

#open dataframe of two tables
ifile1 = get_filehandle(args.table1)
df_ifile1 = pd.read_csv(ifile1, sep="\t")

ifile2 = get_filehandle(args.table2)
df_ifile2 = pd.read_csv(ifile2, sep="\t")

# Merge the two dataframes based on common/index column
outfile_df = pd.merge(df_ifile1, df_ifile2,
             left_on=args.key1,
             right_on=args.key2,
             how=args.how,
             suffixes=(args.suffix1, args.suffix2))

# Output of table1 with new column(s) incld. newcolumns from table2 to terminal
delim = args.delim
outfile_df.to_csv(sys.stdout, index=False, sep=delim)
