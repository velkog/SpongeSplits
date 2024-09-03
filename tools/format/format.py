import logging
from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path
from subprocess import PIPE, Popen, list2cmdline
from sys import exit
from typing import Generator, List

from python.runfiles import Runfiles

from tools.format.system.file import File
from tools.format.system.formatter import ALL_FORMATTERS, IFormatter, RuffFormat, RuffLint
from tools.format.system.print import print_diff, print_error


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--in-place", "-i", help="Inplace edit <file>s, if specified.", action="store_true")
    parser.add_argument("dirs", nargs="+", help="List of files to format.")
    args = parser.parse_args()
    return args


def get_all_files(base_dirs: List[str], formatter_interface: IFormatter) -> List[File]:
    working_dir = Path(environ["BUILD_WORKING_DIRECTORY"])
    assert working_dir.exists()

    all_files = []
    for base_dir in base_dirs:
        full_path = Path(working_dir, base_dir)
        assert full_path.exists()

        for file_glob in formatter_interface.assoc_files():
            all_files.extend([File(file_path) for file_path in full_path.rglob(file_glob) if file_path.is_file()])

    return all_files


def run_format(args: Namespace) -> List[Generator | List[str]]:
    env = {}
    r = Runfiles.Create()
    env.update(r.EnvVars())

    all_diffs = []
    for formatter_interface in ALL_FORMATTERS:
        all_files = get_all_files(args.dirs, formatter_interface)

        for file in all_files:
            cmd = formatter_interface.formatter_cmd(file, args.in_place)
            logging.debug(f"Fomatting {file} with cmd: '{list2cmdline(cmd)}'")
            process = Popen(cmd, stdout=PIPE, universal_newlines=True)
            stdout, _stderr = process.communicate()

            stdout = [line + "\n" for line in stdout.splitlines()]
            if formatter_interface == RuffFormat:
                # Python's Ruff formatter already formats as a diff
                all_diffs.append(stdout)
            elif formatter_interface == RuffLint:
                all_diffs.append([] if "All checks passed!" in stdout[0] else stdout)
            else:
                all_diffs.append(file.diff(stdout))

    return all_diffs


def report(args: Namespace, diffs=List[Generator | List[str]]) -> bool:
    success = True

    if not args.in_place:
        for diff in diffs:
            if not print_diff(diff):
                success = False

    if success:
        logging.info(f"{len(diffs)} files are properly formatted.")

    return success


def main() -> int:
    args = parse_args()
    diffs = run_format(args)
    success = report(args, diffs)
    return 0 if success else 1


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    try:
        status = main()
        exit(status)
    except Exception as e:
        print_error(e)
        raise e
