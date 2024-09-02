from typing import Generator

from termcolor import colored, cprint

def print_diff(diff: Generator[str, None, None]) -> None:
    for diff_line in diff:
        diff_line = diff_line.strip()
        if diff_line[:4] in ['--- ', '+++ ']:
            print(colored(diff_line, attrs=["bold"]))
        elif diff_line.startswith('@@ '):
            print(colored(diff_line, "cyan"))
        elif diff_line.startswith('+'):
            print(colored(diff_line, "green"))
        elif diff_line.startswith('-'):
            print(colored(diff_line, "red"))
        else:
            print(diff_line)

def print_error(error: str, use_colors: bool = True) -> None:
    if use_colors:
        error = colored(error, "red")
