#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from datfile_copier.copier import process as copier_process
from datfile_copier.library import GameLibrary
from datfile_copier.logger import Logger


def validate_required(options):
    if not set(['dat', 'input_dirs', 'output_dir']).issubset(options):
        Logger.error(f'Missing one of required [dat, input_dirs, output_dir] options.')
        sys.exit(2)


def validate_dirs(input_dirs, output_dir):
    check_dirs = input_dirs + [output_dir]
    for directory in check_dirs:
        if not os.path.isdir(directory):
            Logger.error(f'"{directory}" does not exist or is not a directory.')
            sys.exit(2)

    if len(os.listdir(output_dir)) != 0:
        Logger.error(f'"{directory}" is not empty.')
        sys.exit(2)


def process(options):

    if 'verbose' in options:
        Logger.set_level(options['verbose'])

    validate_required(options)
    validate_dirs(options['input_dirs'], options['output_dir'])

    game_library = GameLibrary(options['dat'])

    if 'header_xml' in options:
        game_library.set_header_xml(options['header_xml'])

    if 'region_limit' in options:
        game_library.select_by_region_limit(options['region_limit'])
    else:
        game_library.select_all()

    copier_process(game_library, options['input_dirs'], options['output_dir'])

    have = game_library.get_seen_selected()
    Logger.info(f'Have: {len(have)}')

    missing = game_library.get_missing_selected()
    Logger.info(f'Missing: {len(missing)}')
    for rom in missing:
        Logger.info(f"    {rom['name']}")
