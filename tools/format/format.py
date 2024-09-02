import logging

from argparse import ArgumentParser, Namespace
from os import environ, path
from pathlib import Path
from subprocess import Popen, PIPE, list2cmdline
from sys import exit
from typing import Generator, List
from fnmatch import fnmatch

from python.runfiles import Runfiles

from tools.format.lang.language import ILanguage, CPP
from tools.format.system.file import File
from tools.format.system.print import print_diff, print_error


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--in-place",
        "-i",
        help="Inplace edit <file>s, if specified.",
        action="store_true"
    )
    parser.add_argument(
        "dirs",
        nargs="+", 
        help="List of files to format."
    )
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

def run_format(args: Namespace) -> List[Generator]:
    env = {}
    r = Runfiles.Create()
    env.update(r.EnvVars())

    language = CPP
    all_files = get_all_files(args.dirs, language)

    all_diffs = set()
    for file in all_files:
        runfile_location = r.Rlocation(language.formatter_directory())
        assert runfile_location and path.exists(runfile_location)

        cmds = [runfile_location, str(file)]
        if args.in_place:
            cmds.append("-i")
    
        process = Popen(cmds, env=env, stdout = PIPE, stderr = PIPE, universal_newlines=True)
        process.wait()

        if process.returncode:
            err_str = f"Command '{list2cmdline(cmds)}' returned non-zero exit status {process.returncode}."
            for err in process.stderr.readlines():
                err_str += "\n" + err
            raise SystemError(err_str)
        
        all_diffs.add(file.diff(process.stdout.readlines()))
    
    return all_diffs

def report(args: Namespace, diffs = List[Generator]) -> None:
    if args.in_place:
        logging.info(f"{len(diffs)} files are properly formatted.")
    else:
        for diff in diffs:
            print_diff(diff)


def main() -> None:
    args = parse_args()
    diffs = run_format(args)
    report(args, diffs)


if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO)
    try:
        main()
    except Exception as e:
        print_error(e)
        raise e
    
