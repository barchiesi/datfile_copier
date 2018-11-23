#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import copy
import argparse

import datfile_copier

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
    parser.add_argument('-i', '--input_dir', action='append', dest='input_dirs', required=True, help='One or more input directories', metavar='INPUT_DIR')
    parser.add_argument('-o', '--output_dir', action='store', required=True, help='Output directory (must be empty)', metavar='OUTPUT_DIR')
    parser.add_argument('-d', '--dat', action='store', required=True, help='No-intro dat file', metavar='DAT_FILE')

    parser.add_argument('--header_offset', action='store', type=int, help='Offset in bytes to consider for header removal', metavar='HEADER_OFFSET', default=argparse.SUPPRESS)
    parser.add_argument('--region_limit', action='store', dest='region_limit', required=False, help='Limit to comma separated region list', metavar='REGION_LIMIT', default=argparse.SUPPRESS)

    return parser.parse_args()


if __name__ == '__main__':
    options = vars(parse_args())
    clean_region_limit(options)

    datfile_copier.main(copy.deepcopy(options))
