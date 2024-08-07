import os
import fileinput
import argparse
import subprocess
import time
import sys

argParser = argparse.ArgumentParser()
argParser.add_argument("-cv", "--current_version", help="Current version", required=True)
argParser.add_argument("-nv", "--next_version", help="Specify a version", required=False)
args = argParser.parse_args()


def replace(filename, current_version, new_version):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(current_version, new_version), end='')

def get_new_version(old_release):
    old_version = old_release.rpartition('.')
    old_year = old_version[0]
    old_month = old_version[1]
    old_day = old_version[2]
    next_version = time.strftime("%Y.%m.00").rpartition('.')
    next_year = next_version[0]
    next_month = next_version[1]
    if old_year == next_year and old_month == next_month:
        new_version = time.strftime("%Y.%m.") + str(int(old_day) + 1).zfill(2)
    else:
        new_version = time.strftime("%Y.%m.00")
    return new_version

def set_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)

try:
    current_version = args.current_version
    new_version = args.next_version
    if not new_version:
       new_version = get_new_version(current_version)
    # update
    print("Update version from ",current_version," to ", new_version)

    replace("../publish.gradle", current_version, new_version)
     set_output("TAG", "catalog_v"+new_version)
except Exception as error:
    sys.exit("Did not update version" + error)