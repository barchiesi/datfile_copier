#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

import copier
import library

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
                print(f'ERROR: argument -l/--region_limit: invalid value. Must be comma separated list of:')
                for region in KNOWN_REGIONS:
                    print(f'ERROR:      {region}')
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

    known_games = library.build_known_games(options.dat)

    if options.region_limit:
        wanted_roms = library.build_wanted_roms(known_games, options.region_limit)
    else:
        wanted_roms = library.build_all_roms(known_games)

    copier.process(wanted_roms, options.input_dirs, options.output_dir)

    print('\nHave:')
    for rom in [x for x in wanted_roms.values() if x['seen'] == True]:
        print(f"    {rom['name']}")

    print('\nMissing:')
    for rom in [x for x in wanted_roms.values() if x['seen'] == False]:
        print(f"    {rom['name']}")
