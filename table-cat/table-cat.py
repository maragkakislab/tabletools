#!/usr/bin/env python

"""
Script to concatenate multiple files (table-format) with common header,
also works for gzip files, with output in non-gzip table format.
"""
import sys
import argparse
import gzip

parser = argparse.ArgumentParser()
parser.add_argument("tables", nargs='+',
                    help="Input multiple table with same headers")
parser.add_argument("-z", "--gunzip", action='store_true',
                    help="Decompress files using gzip")
args = parser.parse_args()

def open_filehandle(file, gunzip=False):
    if gunzip:
        return gzip.open(file, "rt")
    else:
        return open(file)

#Get headers
headerlines = []
for file in args.tables:
    infile = open_filehandle(file, args.gunzip)
    first_line = infile.readline()
    headerlines += [first_line.strip()]
    infile.close()

if not all(headers == headerlines[0] for headers in headerlines):
    print("File headers are not same")
    sys.exit(1)
else:
    print(headerlines[0])
    for file in args.tables:
        infile = open_filehandle(file, args.gunzip)
        next(infile)
        for line in infile:
            print(line.strip())
        infile.close()
