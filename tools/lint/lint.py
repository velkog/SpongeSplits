#!/usr/bin/env python
"""
A wrapper script used for executing a given lint/format executable
across multiple files and to use for continuous integration.
"""

from argparse import ArgumentParser, Namespace
from shutil import which
from sys import exit

def parse_args() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lint-executable",
        metavar="EXECUTABLE",
        help="path to the lint executable",
        required=True)
    return parser.parse_args()

def validate_args(args: Namespace) -> None:
    if not which(args.lint_executable):
        raise NameError(f"Given executable '{args.lint_executable}' does not exist.")

def main() -> None:
    try:
        args = parse_args()
        validate_args(args)
    except Exception as e:
        print(e)
        raise e

if __name__ == '__main__':
    exit(main())
