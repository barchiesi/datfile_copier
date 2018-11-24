# datfile_copier
Little program for copying all valid No-Intro roms from one or more input folders to an output folder, according to a specific No-Intro dat file. It also allows specifying what regions to copy in order to create 1G1R rom selections.

Supports specifying a header xml file for skipping certain headers present in roms (eg. Nes, more info [here](http://www.no-intro.org/faq.htm)).

For more information on No-Intro and dat files, please visit [www.no-intro.org](http://www.no-intro.org/).

## Usage
```
usage: main.py [-h] --input_dir INPUT_DIR --output_dir OUTPUT_DIR --dat
               DAT_FILE [--verbose] [--header_xml HEADER_XML]
               [--region_limit REGION_LIMIT]

Extract into output directory all valid roms according to No-intro dat file.

optional arguments:
  -h, --help            show this help message and exit
  --input_dir INPUT_DIR, -i INPUT_DIR
                        one or more input directories
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        output directory (directory must be empty)
  --dat DAT_FILE, -d DAT_FILE
                        no-intro dat file
  --verbose, -v         verbose up to two times
  --header_xml HEADER_XML
                        path to xml with header skipping information
  --region_limit REGION_LIMIT
                        Limit to comma separated region list (ordered by
                        preference)
```

## Examples
Copy all roms in `./some_snes_roms_folder/` to `./valid_roms_folder/` using definitions in `./snes_dat_file.dat`:
```
python main.py -i ./some_snes_roms_folder/ -o ./valid_roms_folder/ -d ./snes_dat_file.dat
```
Same as above but use header xml:
```
python main.py -i ./some_nes_roms_folder/ -o ./valid_roms_folder/ -d ./snes_at_file.dat --header_xml ./No-Intro_NES.xml
```
Same as first example but limit to USA region and if missing EUR region:
```
python main.py -i ./some_snes_roms_folder/ -o ./valid_roms_folder/ -d ./snes_dat_file.dat --region_limit "USA,EUR"
```
### Notes
Tested with snes datfile and nes datfile + headerxml.
