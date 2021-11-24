"""
Concatenate table files that have the same header, similar to the Bash cat
function.
"""

import sys
import argparse
import gzip


def open_filehandle(file, gunzip=False):
    if gunzip:
        return gzip.open(file, "rt")
    else:
        return open(file)


def parse_args(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tables", nargs='+',
                        help="Input table file(s)")
    parser.add_argument("-z", "--gunzip", action='store_true',
                        help="Decompress files using gzip")
    return parser.parse_args(args)


def main():

    args = parse_args(sys.argv[1:])

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
