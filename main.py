#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import argparse

import datfile_copier
from logger import LogLevel

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


def clean_verbosity(options):
    if 'verbose' in options:
        if options['verbose'] == 1:
            options['verbose'] = LogLevel.INFO
        elif options['verbose'] == 2:
            options['verbose'] = LogLevel.DEBUG
        else:
            options['verbose'] = LogLevel.DEBUG


def clean_region_limit(options):
    if 'region_limit' in options:
        raw_region_limit = options['region_limit']
        options['region_limit'] = []
        for region in raw_region_limit.split(','):
            if region in KNOWN_REGIONS:
                options['region_limit'].append(region)
            else:
                print(f'ERROR: argument -l/--region_limit: invalid value. Must be comma separated list of:')
                for region in KNOWN_REGIONS:
                    print(f'ERROR:      {region}')
                sys.exit(2)


def parse_args():
    parser = argparse.ArgumentParser(description='Extract into output directory all valid roms according to No-intro dat file.')
    # Mandatory arguments
    parser.add_argument('--input_dir', '-i', action='append', dest='input_dirs', required=True, help='one or more input directories', metavar='INPUT_DIR')
    parser.add_argument('--output_dir', '-o', action='store', required=True, help='output directory (directory must be empty)', metavar='OUTPUT_DIR')
    parser.add_argument('--dat', '-d', action='store', required=True, help='no-intro dat file', metavar='DAT_FILE')

    # Optional arguments
    parser.add_argument('--verbose', '-v', action='count', help='verbose up to two times', default=argparse.SUPPRESS)
    parser.add_argument('--header_offset', action='store', type=int, help='offset in bytes to consider for header ignoring', metavar='HEADER_OFFSET', default=argparse.SUPPRESS)
    parser.add_argument('--region_limit', action='store', dest='region_limit', required=False, help='Limit to comma separated region list (ordered by preference)', metavar='REGION_LIMIT', default=argparse.SUPPRESS)

    return parser.parse_args()


if __name__ == '__main__':
    options = copy.deepcopy(vars(parse_args()))
    clean_verbosity(options)
    clean_region_limit(options)

    datfile_copier.main(options)
