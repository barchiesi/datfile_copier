import os
import shutil
from zipfile import ZipFile, is_zipfile, ZIP_LZMA
import hashlib


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
            print(f'DEBUG: Duplicate rom "{rom_entry["rom_filename"]}" at "{rompath}" with md5 "{md5sum}"')
            return

        copy_zipped(rompath, rom_entry, output_dir)

    except PermissionError as e:
        print(f'DEBUG: Failed reading rom at "{rompath}": {e}')
        return
    except IndexError:
        print(f'DEBUG: Empty zip at "{rompath}"')
        return
    except KeyError:
        print(f'DEBUG: Unknown rom at "{rompath}" with md5 "{md5sum}"')
        return


def iterate_roms(input_dirs):
    for input_dir in input_dirs:
        for input_file in os.scandir(input_dir):
            yield input_file.path


def process(wanted_roms, input_dirs, output_dir):
    for rompath in iterate_roms(input_dirs):
        handle_rompath(rompath, wanted_roms, output_dir)
