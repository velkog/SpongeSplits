#!/usr/bin/env python
"""
A wrapper script used for executing a given lint/format executable
across multiple files and to use for continuous integration.
"""

from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from difflib import unified_diff
from fnmatch import fnmatch
from functools import partial
from io import open
from shutil import which
from subprocess import list2cmdline, Popen, PIPE
from multiprocessing import cpu_count, Pool
from os import environ, path, walk
from sys import exit
from typing import List, Generator, Optional

from tools.print import print_diff, print_error

WORKING_DIR = environ["BUILD_WORKING_DIRECTORY"]

class Languages:
    CPP = "cpp"

    @classmethod
    def get_all_options(cls) -> List[str]:
        options = []
        for attribute_name in dir(cls):
            if not attribute_name.startswith("__"):
                attribute = getattr(cls, attribute_name)
                if not isinstance(attribute, Callable):
                    options.append(getattr(cls, attribute_name))
        return options


LANGUAGE_EXTENSIONS = {
    Languages.CPP: [
        "c",
        "c++",
        "cc",
        "cpp",
        "cxx",
        "h",
        "h++",
        "hh",
        "hpp",
        "hxx",
    ]
}

class LintFile:
    errs: Optional[List[str]] = None
    is_linted: bool = False
    original: Optional[List[str]] = None
    reformatted: Optional[List[str]] = None

    def __init__(self, file_name: str) -> None:
        self.file = file_name
        with open(file_name, "r", encoding="utf-8") as f:
            self.original = f.readlines()

    def require_linted(func: Callable):
        def wrapper(self, *args, **kwargs):
            if self.is_linted:
                return func(self, *args, **kwargs)
            else:
                raise ValueError(f"File '{self.file}' must be linted before calling '{func.__name__}'.")
        return wrapper

    def run_lint(self, exc: str) -> None:
        command = [exc, self.file]
        proc = Popen(
            command,
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True,
        )
        proc.wait()

        if proc.returncode:
            err_str = f"Command '{list2cmdline(exc)}' returned non-zero exit status {proc.returncode}."
            for err in proc.stderr.readlines():
                err_str += "\n" + err
            raise SystemError(err_str)

        self.reformatted = list(proc.stdout.readlines())
        self.errs = list(proc.stderr.readlines())
        self.is_linted: bool = True

    @require_linted
    def get_diff(self) -> Generator[str, None, None]:
        return unified_diff(
            self.original,
            self.reformatted,
            fromfile=f"{self.file}\toriginal",
            tofile=f"{self.file}\treformatted",
        )
    

def parse_args() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("paths", metavar="path", nargs="+")
    parser.add_argument(
        "--lint-executable",
        metavar="EXECUTABLE",
        help="path to the lint executable",
        required=True)
    parser.add_argument(
        "--language",
        help="Language for seleceting file extensions",
        choices=Languages.get_all_options(),
        required=True)
    return parser.parse_args()

def validate_args(args: Namespace) -> None:
    if not which(args.lint_executable):
        raise NameError(f"Given executable '{args.lint_executable}' does not exist.")
    
    for files_path in args.paths:
        full_path = path.join(WORKING_DIR, files_path)
        if not path.exists(full_path):
            raise NameError(f"Given path '{full_path}' does not exist.")

def get_paths_files(paths: List[str], language: str) -> List[str]:
    extensions = set(LANGUAGE_EXTENSIONS[language])
    exclude = set()

    files = []
    for files_path in paths:
        full_path = path.join(WORKING_DIR, files_path)
        
        if not path.isdir(full_path):
            files.append(full_path)
            continue

        for dirpath, dnames, fnames in walk(full_path):
            fpaths = [path.join(dirpath, fname) for fname in fnames]
            for pattern in exclude:
                # os.walk() supports trimming down the dnames list
                # by modifying it in-place,
                # to avoid unnecessary directory listings.
                dnames[:] = [
                    x for x in dnames
                    if
                    not fnmatch.fnmatch(path.join(dirpath, x), pattern)
                ]
                fpaths = [
                    x for x in fpaths if not fnmatch.fnmatch(x, pattern)
                ]
            for f in fpaths:
                ext = path.splitext(f)[1][1:]
                if ext.lower() in extensions:
                    files.append(f)
        
    return files

def run_lint(exc: str, file: str) -> LintFile:
    lint_file = LintFile(file)
    lint_file.run_lint(exc)
    return lint_file

def run(exc: str, language: str, paths: List[str]) -> List[LintFile]:
    files = get_paths_files(paths, language)
    num_pools = min(cpu_count() + 1, len(files))

    with Pool(num_pools) as pool:
        linted_files = [file for file in pool.imap_unordered(partial(run_lint, exc), files)]
    return linted_files

def report(linted_files: List[LintFile]) -> None:
    for file in linted_files:
        print_diff(file.get_diff())

def main() -> None:
    try:
        args = parse_args()
        validate_args(args)
        linted_files = run(args.lint_executable, args.language, args.paths)
        report(linted_files)

    except Exception as e:
        print_error(e)
        raise e

if __name__ == "__main__":
    exit(main())
