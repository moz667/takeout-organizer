#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import os
import sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

def main(argv):
    takeout_directory = ''
    archive_directory = ''
    dry_run = False

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["idir=","odir=","dry_run"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-i", "--idir"):
            takeout_directory = arg
        elif opt in ("-o", "--odir"):
            archive_directory = arg
        elif opt in "--dry_run":
            dry_run = True

    if takeout_directory == "" or archive_directory == "":
        print_help()
        sys.exit(2)



    sys.exit(0)

def print_help():
    print('takeout-organizer.py -i <takeout_directory> -o <archive_directory>')
    print('takeout-organizer.py --idir=<takeout_directory> --odir=<archive_directory>')

if __name__ == "__main__":
   main(sys.argv[1:])