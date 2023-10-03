#!/usr/bin/env python3

import argparse
import csv
import os
import platform
import subprocess
import traceback

if platform.system() == 'Windows':
    OPENSCAD = 'C:\Program Files\OpenSCAD\openscad.exe'
elif platform.system() == 'Linux':
     OPENSCAD = 'openscad'
else:
    OPENSCAD = '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'

MYDIR = os.path.dirname(os.path.realpath(__file__))

expected_fields = ("Brand", "Type", "Type2", "Color", "Color2", "Bed Temp", "Hotend Temp")

def gen_samples():
    # Ensure output directory exists
    output_dir = f"{MYDIR}/{args.output_dir}"
    os.makedirs(output_dir, exist_ok=True)

    # Open the input file and read line by line
    input_filename = f"{MYDIR}/{args.input_file}"
    with open(input_filename, 'r', encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        # Make sure the file is formatted as expected
        if set(expected_fields).intersection(set(reader.fieldnames)) != set(expected_fields):
            print("CSV file column headers do not match expected values.")
            print(f"Expected: {expected_fields}")
            print(f"Found:    {reader.fieldnames}")
            exit(1)
        for line in reader:
            # Skip empty lines
            if len("".join(v for v in line.values())) <= 0:
                continue
            print(f"Processing {line}")
            output_filename = output_dir + "/" + "_".join((v for v in line.values() if v)) + ".stl"
            # If the file exists, save time by not re-creating it
            if os.path.exists(output_filename):
                print(f"    {output_filename} already exists")
            else:
                # Run openscad with the values from this line in the input file
                subprocess.run(
                    [OPENSCAD,
                    '-o', output_filename,
                    '-D', f'BRAND="{line["Brand"]}"',
                    '-D', f'TYPE="{line["Type"]}"',
                    '-D', f'TYPE2="{line["Type2"]}"',
                    '-D', f'COLOR="{line["Color"]}"',
                    '-D', f'COLOR2="{line["Color2"]}"',
                    '-D', f'TEMP_BED="{line["Bed Temp"]}"',
                    '-D', f'TEMP_HOTEND="{line["Hotend Temp"]}"',
                    f'{MYDIR}/FilamentSamples.scad',
                    ], check=True)
                print()

if __name__ == "__main__":
    print()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", "-i", type=str, default="samples.csv", required=False, help="The path to the CSV file containing the filament info")
    parser.add_argument("output_dir", default="stl", nargs="?", help="output directory to put the STL files into. Must be relative to the script directory")
    args = parser.parse_args()

    try:
        gen_samples()
    except Exception:
        traceback.print_exc()
        input("Press Enter to continue...")
    finally:
        print()
