import logging

from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path
from subprocess import Popen, PIPE, list2cmdline
from sys import exit
from typing import Generator, List

from python.runfiles import Runfiles

from tools.format.lang.language import ILanguage, ALL_LANGUAGES, Python
from tools.format.system.file import File
from tools.format.system.print import print_diff, print_error


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--in-place", "-i", help="Inplace edit <file>s, if specified.", action="store_true")
    parser.add_argument("dirs", nargs="+", help="List of files to format.")
    args = parser.parse_args()
    return args


def get_all_files(base_dirs: List[str], language: ILanguage) -> List[File]:
    working_dir = Path(environ["BUILD_WORKING_DIRECTORY"])
    assert working_dir.exists()

    all_files = []
    for base_dir in base_dirs:
        full_path = Path(working_dir, base_dir)
        assert full_path.exists()

        for file_glob in language.assoc_files():
            all_files.extend([File(file_path) for file_path in full_path.rglob(file_glob) if file_path.is_file()])

    return all_files


def run_format(args: Namespace) -> List[Generator | List[str]]:
    env = {}
    r = Runfiles.Create()
    env.update(r.EnvVars())

    all_diffs = []
    for language in ALL_LANGUAGES:
        all_files = get_all_files(args.dirs, language)

        for file in all_files:
            cmd = language.formatter_cmd(file, args.in_place)
            logging.debug(f"Fomatting {file}")
            process = Popen(cmd, env=env, stdout=PIPE, stderr=PIPE, universal_newlines=True)
            process.wait()

            if language == Python:
                # Python's Ruff formatter already formats as a diff
                all_diffs.append(process.stdout.readlines())
            else:
                all_diffs.append(file.diff(process.stdout.readlines()))

    return all_diffs


def report(args: Namespace, diffs=List[Generator | List[str]]) -> bool:
    success = True
    if args.in_place:
        logging.info(f"{len(diffs)} files are properly formatted.")
    else:
        for diff in diffs:
            if not print_diff(diff):
                success = False
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
        level=logging.INFO,
    )
    try:
        status = main()
        exit(status)
    except Exception as e:
        print_error(e)
        raise e
