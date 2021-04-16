#!/usr/bin/env python

"""
Add a column containing a constant value to a table. Header assumed.
"""

import sys
import argparse 

def get_input_file_object(filename):
    if filename == "-":
        return sys.stdin
    return open(filename, "r")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-t", "--table", default='-', help="input csv file; STDIN if - (default: %(default)s")
parser.add_argument("-c", "--col-name", required=True, help="name for new column")
parser.add_argument("-v", "--col-value", required=True, help="constant value for new column")
parser.add_argument("-s", "--separator", default='\t', help="column separator character, default: <TAB>")
parser.add_argument("--at-end", action="store_true", help="inserts new column as the right most one.")
args = parser.parse_args()


table = get_input_file_object(args.table)
    
def add_col(sep, colname, colvalue, at_end):
    i = 0
    for line in table:
        if i==0:
            line = line.rstrip('\n')
            if at_end:
                print(line + sep + colname)
            print(colname + sep + line)
        else:
            line = line.rstrip('\n')
            if at_end:
                print(line + sep + colvalue)
            print(colvalue + sep + line)
        i += 1

    return

add_col(args.separator, args.col_name, args.col_value, args.at_end)
