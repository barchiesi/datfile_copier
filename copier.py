import os
import shutil
from zipfile import ZipFile, is_zipfile, ZIP_LZMA
import hashlib
import xml.etree.ElementTree as ET


def copy_zipped(rompath, rom_entry, output_dir):
    final_filename = os.path.splitext(rom_entry['filename'])[0]+'.zip'
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


def handle_rompath(rompath, known_roms, output_dir):
    try:
        md5sum = compute_md5(rompath)
        rom_entry = known_roms[md5sum.lower()]

        if rom_entry['seen']:
            print(f'INFO: Duplicate rom "{rom_entry["filename"]}" at "{rompath}" with md5 "{md5sum}"')
            return

        copy_zipped(rompath, rom_entry, output_dir)
        print(f'INFO: Known rom "{rom_entry["filename"]}" at "{rompath}" with md5 "{md5sum}"')

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


def build_known_roms(filename):
    known_roms = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for game_tag in root.findall('.//game'):
        rom_tag = game_tag.find('.//rom')
        rom_md5 = rom_tag.attrib['md5']
        rom_filename = rom_tag.attrib['name']

        if not rom_tag and not rom_filename:
            print(f'Error for game, missing one of md5: "{rom_md5}" or filename: "{rom_filename}"')
            continue

        if rom_md5 in known_roms:
            print(f'Error for game, already existing md5: "{rom_md5}" for filename: "{rom_filename}"')
            continue

        known_roms[rom_md5.lower()] = {
            'filename': rom_filename,
            'seen': False
        }

    return known_roms


def process(input_dirs, output_dir, dat_file):
    known_roms = build_known_roms(dat_file)

    for rompath in iterate_roms(input_dirs):
        handle_rompath(rompath, known_roms, output_dir)
