import sys
import argparse
from wyvern import __version__

parser = argparse.ArgumentParser()
parser.add_argument("-V", "-v", "--version", help="Check the version of library.", action="store_true")


def main() -> None:
    args = parser.parse_args()
    if args.version is True:
        print("Library version: ", __version__, "\nPython version: ", sys.version)


main()
