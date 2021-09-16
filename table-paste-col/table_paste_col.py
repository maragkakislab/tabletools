#!/usr/bin/env python

"""
Add a column containing a constant value to a table. Header assumed.
"""

import sys
import argparse


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-t", "--table", default='-',
                    help="Input table; STDIN if - (default: %(default)s")
parser.add_argument("-c", "--col-name", required=True,
                    help="Name for new column")
parser.add_argument("-v", "--col-value", required=True,
                    help="Constant value for new column")
parser.add_argument("-s", "--separator", default='\t',
                    help="Column separator character, default: <TAB>")
parser.add_argument("--at-end", action="store_true",
                    help="Insert new column at right most column.")
args = parser.parse_args()

def get_input_file_object(filename):
    if filename == "-":
        return sys.stdin
    return open(filename, "r")

table = get_input_file_object(args.table)

def add_col(sep, colname, colvalue, at_end):
    i = 0
    for line in table:
        if i==0:
            line = line.rstrip('\n')
            if at_end:
                print(line + sep + colname)
            else:
                print(colname + sep + line)
        else:
            line = line.rstrip('\n')
            if at_end:
                print(line + sep + colvalue)
            else:
                print(colvalue + sep + line)
        i += 1
    return

add_col(args.separator, args.col_name, args.col_value, args.at_end)
