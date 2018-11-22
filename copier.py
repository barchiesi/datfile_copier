import os
import shutil
from zipfile import ZipFile, is_zipfile, ZIP_LZMA
import hashlib
import xml.etree.ElementTree as ET


def copy_zipped(rompath, rom_entry, output_dir):
    final_filename = os.path.splitext(rom_entry['rom_filename'])[0]+'.zip'
    finalpath = os.path.join(output_dir, final_filename)

    if is_zipfile(rompath):
        shutil.copy2(rompath, finalpath)
    else:
        with ZipFile(finalpath, mode='x', compression=ZIP_LZMA) as zipped_rom:
            zipped_rom.write(rompath)

    rom_entry['seen'] = True


def compute_md5(rompath):
    md5sum = hashlib.md5()

    if is_zipfile(rompath):
        with ZipFile(rompath) as zipped_rom:
            first_zip_entry = zipped_rom.infolist()[0]
            rom = zipped_rom.read(first_zip_entry)
            md5sum.update(rom)
    else:
        with open(rompath, 'rb') as rom:
            md5sum.update(rom.read())

    return md5sum.hexdigest()


def handle_rompath(rompath, wanted_roms, output_dir):
    try:
        md5sum = compute_md5(rompath)
        rom_entry = wanted_roms[md5sum.lower()]

        if rom_entry['seen']:
            print(f'INFO: Duplicate rom "{rom_entry["rom_filename"]}" at "{rompath}" with md5 "{md5sum}"')
            return

        copy_zipped(rompath, rom_entry, output_dir)
        print(f'INFO: Known rom "{rom_entry["rom_filename"]}" at "{rompath}" with md5 "{md5sum}"')

    except PermissionError as e:
        print(f'INFO: Failed reading rom at "{rompath}": {e}')
        return
    except IndexError:
        print(f'INFO: Empty zip at "{rompath}"')
        return
    except KeyError:
        print(f'INFO: Unknown rom at "{rompath}" with md5 "{md5sum}"')
        return


def iterate_roms(input_dirs):
    for input_dir in input_dirs:
        for input_file in os.scandir(input_dir):
            yield input_file.path


def build_all_roms(known_games):
    wanted_roms = {}
    for game_clones in known_games.values():
        for game in game_clones:
            wanted_roms[game['rom_md5']] = game
    return wanted_roms


def build_wanted_roms(known_games, region_limit):
    wanted_roms = {}
    for game_clones in known_games.values():
        found = False
        for region in region_limit:
            for game in game_clones:
                if 'region' not in game:
                    break
                if game['region'] == region:
                    wanted_roms[game['rom_md5']] = game
                    found = True
                    break

            if found:
                break

    return wanted_roms


def build_known_games(filename):
    known_games = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for game_elem in root.findall('.//game'):
        game = {
            'name': game_elem.attrib['name'],
            'seen': False
        }
        if 'cloneof' in game_elem.attrib:
            game_key = game_elem.attrib['cloneof']
        else:
            game_key = game['name']

        game_release_elem = game_elem.find('.//release')
        if game_release_elem != None:
            game['region'] = game_release_elem.attrib['region']

        rom_elem = game_elem.find('.//rom')
        game['rom_md5'] = rom_elem.attrib['md5']
        game['rom_filename'] = rom_elem.attrib['name']

        game_clones = known_games.get(game_key, [])
        game_clones.append(game)
        known_games[game_key] = game_clones

    return known_games


def process(input_dirs, output_dir, dat_file, region_limit):
    known_games = build_known_games(dat_file)

    if region_limit:
        wanted_roms = build_wanted_roms(known_games, region_limit)
    else:
        wanted_roms = build_all_roms(known_games)

    for rompath in iterate_roms(input_dirs):
        handle_rompath(rompath, wanted_roms, output_dir)
