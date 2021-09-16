#!/usr/bin/env python
"""
Select (from all columns) and/or reorder (re-arrange) table columns using
column name or column-number, can be used to drop columns as well from table.
"""

import sys
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-i", "--table",
                    help="Input file with multiple columns")
parser.add_argument("-t", "--cols-name-or-number", default='name',
                    help="index name type of column eitehr name or number, (default: %(default)s)")
parser.add_argument("-c", "--cols-to-select", nargs='+',
                    help="Name or number of column(s) to drop from input file")
parser.add_argument("-d", "--idelim", default="\t",
                    help="Delimiter of the input file, (default: <TAB>)")
parser.add_argument("-o", "--odelim", default="\t",
                    help="Delimiter for the output file, (default: <TAB>)")
args = parser.parse_args()

def get_filehandle(filename):
    """ Returns a filehandle """
    if filename == "-":
        return sys.stdin
    return open(filename, "r")

ifile = get_filehandle(args.table)

df = pd.read_csv(ifile, sep=args.idelim)

if args.cols_name_or_number == "name":
    df_out = df[args.cols_to_select]
elif args.cols_name_or_number == "number":
    col_list = list(map(int, args.cols_to_select))
    df_out = df.iloc[:, col_list]
else:
    print("Please specify number or name of column to drop")
    sys.exit(0)

df_out.to_csv(sys.stdout, index=False, sep=args.odelim)
