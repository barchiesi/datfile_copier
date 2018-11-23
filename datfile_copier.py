#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import copier
import library


def validate_required(options):
    if not set(['dat', 'input_dirs', 'output_dir']).issubset(options):
        sys.stderr.write(f'ERROR: Missing one of required [dat, input_dirs, output_dir] options.\n')
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


def main(options):

    validate_required(options)
    validate_dirs(options['input_dirs'], options['output_dir'])

    known_games = library.build_known_games(options['dat'])

    if 'region_limit' in options:
        wanted_roms = library.build_wanted_roms(known_games, options['region_limit'])
    else:
        options['region_limit'] = None
        wanted_roms = library.build_all_roms(known_games)

    copier.process(wanted_roms, options['input_dirs'], options['output_dir'], options['header_offset'])

    have = [x for x in wanted_roms.values() if x['seen'] == True]
    print(f'\nHave: {len(have)}')

    missing = [x for x in wanted_roms.values() if x['seen'] == False]
    print(f'Missing: {len(missing)}')
    for rom in missing:
        print(f"    {rom['name']}")
