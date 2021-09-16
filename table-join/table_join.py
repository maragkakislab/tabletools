#!/usr/bin/env python

"""
Join two tables based on a common key column. Assumes that the input file has a
header line with column names.
"""
import argparse
import sys
import pandas as pd

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-t","--ifile1",
                    help = "Input file one of multiple columns ")
parser.add_argument("-g","--ifile2",
                    help = "Input file two with one common key column")
parser.add_argument("-c","--key-col-file1", default= "key-value",
                    help = "Name of common (key) column first file, (default: %(default)s)")
parser.add_argument("-d","--key-col-file2", default= "key-value",
                    help = "Name of common (key) column second file, (default: %(default)s)")
parser.add_argument("-s", "--delim", default="\t",
                    help="Delimiter of the output file, (default: <TAB>")
parser.add_argument("-k","--how-key", default= "inner",
                    help = "Merge two tables using pandas dataframe.merge option")
args = parser.parse_args()

def get_filehandle(filename):
    """ Returns a filehandle """
    if filename == "-":
        return sys.stdin
    return open(filename, "r")

#Condition for NOT taking both input files (file1 & file2) via stdin
if args.ifile1 == "-" and  args.ifile2 == "-":
    print("Error: can't provide stdin twice as input", file=sys.stderr)
    sys.exit(1)

#open are dataframe the two files file1( transcript - count ) and file2(transcriptid - geneid)
ifile1 = get_filehandle(args.ifile1)
df_ifile1 = pd.read_csv(ifile1, sep="\t")

ifile2 = get_filehandle(args.ifile2)
df_ifile2 = pd.read_csv(ifile2, sep="\t")

# Merge the two dataframes based on common/index column
outfile_df = pd.merge(df_ifile1, df_ifile2,
    left_on=args.key_col_file1, right_on=args.key_col_file2, how=args.how_key)

# Output of file1 with new column(s) incld. geneids from file2 to terminal
delim = args.delim
outfile_df.to_csv(sys.stdout, index=False, sep=delim)
