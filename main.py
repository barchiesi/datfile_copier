#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from copier import process

KNOWN_REGIONS = [
'ASI',
'AUS',
'BRA',
'CAN',
'CHN',
'EUR',
'FRA',
'GER',
'HOL',
'ITA',
'JPN',
'KOR',
'SPA',
'SWE',
'USA',
]


def clean_region_limit(options):
    if options.region_limit is not None:
        raw_region_limit = options.region_limit
        options.region_limit = []
        for region in raw_region_limit.split(','):
            if region in KNOWN_REGIONS:
                options.region_limit.append(region)
            else:
                print(f'main.py: error: argument -l/--region_limit: invalid value. Must be comma separated list of:')
                for region in KNOWN_REGIONS:
                    print(f'main.py: error: argument -l/--region_limit:     {region}')
                sys.exit(2)


def validate_dirs(input_dirs, output_dir):
    check_dirs = input_dirs + [output_dir]
    for directory in check_dirs:
        if not os.path.isdir(directory):
            sys.stderr.write(f'ERROR: "{directory}" does not exist or is not a directory.\n')
            sys.exit(2)

    if len(os.listdir(output_dir)) != 0:
        sys.stderr.write(f'ERROR: "{directory}" is not empty.\n')
        sys.exit(2)


def parse_args():
    parser = argparse.ArgumentParser(description='Extract into output directory all valid roms according to No-intro dat file.')
    parser.add_argument('-l', '--region_limit', action='store', dest='region_limit', required=False, help='Limit to comma separated region list', metavar='REGION_LIMIT')
    parser.add_argument('-i', '--input_dir', action='append', dest='input_dirs', required=True, help='One or more input directories', metavar='INPUT_DIR')
    parser.add_argument('-o', '--output_dir', action='store', required=True, help='Output directory (must be empty)', metavar='OUTPUT_DIR')
    parser.add_argument('-d', '--dat', action='store', required=True, help='No-intro dat file', metavar='DAT_FILE')

    return parser.parse_args()


if __name__ == '__main__':
    options = parse_args()
    clean_region_limit(options)
    validate_dirs(options.input_dirs, options.output_dir)

    process(options.input_dirs, options.output_dir, options.dat, options.region_limit)
