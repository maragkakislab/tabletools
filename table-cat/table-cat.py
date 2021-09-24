#!/usr/bin/env python

"""
Script to concatenate multiple files (table-format) with common header,
also works for gzip files, with output in non-gzip table format.
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

#Get headers
headerlines = []
if args.gzipped:
    for file in args.tables:
        with gzip.open(file, 'rb') as infile:
            first_line = infile.readline().decode('ascii')
            headerlines += [first_line.strip()]
else:
    for file in args.tables:
        with open(file) as infile:
            first_line = infile.readline()
            headerlines += [first_line.strip()]

if all(headers == headerlines[0] for headers in headerlines):
    print(headerlines[0])
    if args.gzipped:
        for file in args.tables:
            with gzip.open(file, 'rb') as infile:
                next(infile)
                for line in infile:
                    print(line.decode('ascii').strip())
    else:
        for file in args.tables:
            with open(file) as infile:
                next(infile)
                for line in infile:
                    print(line.strip())
else:
    print("File headers are not same")
    sys.exit(1)
