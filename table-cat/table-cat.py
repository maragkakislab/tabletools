#!/usr/bin/env python

"""
Script to concatenate multiple files with common header.
"""
import sys
import argparse
import gzip

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--tables", nargs='*',
                    help="Input multiple table with same headers")
parser.add_argument("-z", "--gzipped", action='store_true',
                    help="Use this option for zipped files")
args = parser.parse_args()

##################################################################
#FIXME: Add stdin option
# def get_filehandle(filename):
#     """ Returns a filehandle """
#     if filename == "-":
#         return sys.stdin
#     return open(filename, "r")
#
# ifile = get_filehandle(args.table)
#
# df = pd.read_csv(ifile, sep=args.idelim)
##################################################################

#Get headers
headerlines = []
if args.gzipped:
    for file in args.table:
        with gzip.open(file, 'rb') as infile:
            first_line = infile.readline().decode('ascii')
            headerlines += [first_line.strip()]
else:
    for file in args.table:
        with open(file) as infile:
            first_line = infile.readline()
            headerlines += [first_line.strip()]

for header1, header2 in zip(headerlines, headerlines[1:]):
    if header1 != header2:
        print("File headers are not same")
        sys.exit(1)
    else:
        print(header1)
        if args.gzipped:
            for file in args.table:
                with gzip.open(file, 'rb') as infile:
                    next(infile)
                    for line in infile:
                        print(line.decode('ascii').strip())
        else:
            for file in args.table:
                with open(file) as infile:
                    next(infile)
                    for line in infile:
                        print(line.strip())
