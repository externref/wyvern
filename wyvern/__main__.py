import argparse
import sys

import colorama

from wyvern import __version__

parser = argparse.ArgumentParser(
    prog="wyvern", description="Commands related to the library and it's usage.", add_help=True
)
parser.add_argument("-V", "-v", "--version", help="Check the version of library.", action="store_true")


def main() -> None:
    args = parser.parse_args()
    if args.version is True:
        print(colorama.Fore.LIGHTCYAN_EX, end="")
        print(
            "Library version:",
            colorama.Style.BRIGHT,
            __version__,
            colorama.Style.NORMAL,
            "\nPython version:",
            colorama.Style.BRIGHT,
            sys.version,
            colorama.Style.RESET_ALL,
        )


main()
