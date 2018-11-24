import os
import shutil
from zipfile import ZipFile, is_zipfile, ZIP_LZMA
import hashlib

from logger import Logger


def write_zipped(rom_content, rom_filename, final_path):
    with ZipFile(final_path, mode='x', compression=ZIP_LZMA) as zipped_rom:
        zipped_rom.writestr(rom_filename, rom_content)


def copy_zipped(rom_path, final_path):
    if is_zipfile(rom_path):
        shutil.copy2(rom_path, final_path)
    else:
        with ZipFile(final_path, mode='x', compression=ZIP_LZMA) as zipped_rom:
            zipped_rom.write(rom_path)



def get_rom_content(rom_path):
    if is_zipfile(rom_path):
        with ZipFile(rom_path) as zipped_rom:
            first_zip_entry = zipped_rom.infolist()[0]
            rom = zipped_rom.read(first_zip_entry)
            return rom
    else:
        with open(rom_path, 'rb') as rom:
            return rom.read()


def compute_md5(rom_content, header_offset = None):
    md5sum = hashlib.md5()
    md5sum.update(rom_content)
    return md5sum.hexdigest().lower()


def handle_rompath(rom_path, game_library, output_dir, header_rules = []):
    try:
        rom_content = get_rom_content(rom_path)
    except IndexError:
        Logger.debug(f'Empty zip at "{rom_path}"')
        return
    except PermissionError as e:
        Logger.debug(f'Failed reading rom at "{rom_path}": {e}')
        return

        md5sum_nohead.update(rom_content[header_offset:])
    md5sums = []

    md5sum_original = compute_md5(rom_content)
    md5sums.append(md5sum_original)

    for header_rule in header_rules:
        stripped_rom_content = header_rule.strip_header_from_rom(rom_content)
        if stripped_rom_content:
            Logger.debug(f'Found possible stripped header rom')
            md5sum = compute_md5(stripped_rom_content)
            md5sums.append(md5sum)

    for md5sum in md5sums:
        rom_entry = game_library.get_by_md5sum(md5sum)

        if not rom_entry:
            Logger.debug(f'File at "{rom_path}" with md5sum "{md5sum}" not recognized')
            continue

        if not rom_entry['selected']:
            Logger.debug(f'Ignoring unselected rom at "{rom_path}"')
            continue

        if rom_entry['seen']:
            Logger.debug(f'Duplicate rom at "{rom_path}" for {rom_entry["rom_filename"]}')
            continue

        final_filename = os.path.splitext(rom_entry['rom_filename'])[0]+'.zip'
        final_path = os.path.join(output_dir, final_filename)

        copy_zipped(rom_path, final_path)

        rom_entry['seen'] = True
        Logger.info(f'Found {rom_entry["rom_filename"]} at "{rom_path}"')
        break


def iterate_roms(input_dirs):
    work_dirs = list(input_dirs)

    idx = 0
    while idx < len(work_dirs):
        input_dir = work_dirs[idx]
        Logger.info(f'Scanning dir {input_dir}')
        for input_file in os.scandir(input_dir):
            if input_file.is_dir():
                Logger.debug(f'Adding {input_file} to scan queue')
                work_dirs.append(input_file)
            elif input_file.is_file():
                Logger.debug(f'Yielding {input_file} from scan queue')
                yield input_file.path

        idx += 1


def process(game_library, input_dirs, output_dir):
    header_rules = game_library.get_header_rules()
    for rom_path in iterate_roms(input_dirs):
        handle_rompath(rom_path, game_library, output_dir, header_rules)
