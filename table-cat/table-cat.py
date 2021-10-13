#!/usr/bin/env python

"""
Script to concatenate multiple files (table-format) with common header,
also works for gzip files, with output in non-gzip table format.
"""
import sys
import argparse
import gzip

parser = argparse.ArgumentParser()
parser.add_argument("tables", nargs='*',
                    help="Input multiple table with same headers")
parser.add_argument("-z", "--gunzip", action='store_true',
                    help="Decompress files using gzip")
args = parser.parse_args()

#FIXME:
# def open_filehandle(file, gunzip)


#Get headers
headerlines = []
if args.gunzip:
    for file in args.tables:
        with gzip.open(file, 'rt') as infile:
            first_line = infile.readline()
            headerlines += [first_line.strip()]
else:
    for file in args.tables:
        with open(file) as infile:
            first_line = infile.readline()
            headerlines += [first_line.strip()]

if not all(headers == headerlines[0] for headers in headerlines):
    print("File headers are not same")
    sys.exit(1)
else:
    print(headerlines[0])
    if args.gunzip:
        for file in args.tables:
            with gzip.open(file, 'rt') as infile:
                next(infile)
                for line in infile:
                    print(line.strip())
    else:
        for file in args.tables:
            with open(file) as infile:
                next(infile)
                for line in infile:
                    print(line.strip())
