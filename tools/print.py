from typing import List

from termcolor import colored, cprint


def print_diff(diff: List[str]) -> None:
    for diff_line in diff:
        if diff_line[:4] in ["--- ", "+++ "]:
            print(colored(diff_line, attrs=["bold"]))
        elif diff_line.startswith("@@ "):
            print(colored(diff_line, "cyan"))
        elif diff_line.startswith("+"):
            print(colored(diff_line, "green"))
        elif diff_line.startswith("-"):
            print(colored(diff_line, "red"))
        else:
            print(diff_line)


def print_error(error: str, use_colors: bool = True) -> None:
    if use_colors:
        error = colored(error, "red")
    print(f"{error}")
