"""Main module for Windows converter."""
from pathlib import Path

from psiutils.icecream_init import ic_init

from windows_converter.modules import check_imports
from windows_converter.root import Root

ic_init()


def main():
    check_imports('windows_converter', Path(__file__).parent)
    Root()


if __name__ == '__main__':
    main()
