#! usr/bin/env python
import sys
import argparse 

"""
Add a column containing a constant value to a table. Header assumed. 
"""
def get_input_file_object(filename):
    if filename == "-":
        return sys.stdin
    return open(filename, "r")

parser = argparse.ArgumentParser(description= __doc__)
parser.add_argument("-t", "--table", default='-', help="input csv file; STDIN if - (default: %(default)s")
parser.add_argument("-c", "--colname", help="name for new column")
parser.add_argument("-v", "--colvalue", help="constant value for new column")
parser.add_argument("-s", "--separator", help="column separator character. use $ as prefix")
args = parser.parse_args()

table = get_input_file_object(args.table)
    
def add_col(sep, colname, colvalue):
    i = 0
    for line in table:
        if i==0:
            line = line.rstrip('\n')
            print(line + colname)
        else:
            line = line.rstrip('\n')
            print(line + sep + colvalue)
        i += 1

    return

add_col(args.separator, args.colname, args.colvalue)
