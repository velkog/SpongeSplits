from typing import Generator

from termcolor import colored, cprint


def print_diff(diff: Generator[str, None, None]) -> bool:
    lines = 0
    for diff_line in diff:
        lines += 1
        diff_line = diff_line.strip()
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

    return lines == 0


def print_error(error: str, use_colors: bool = True) -> None:
    if use_colors:
        error = colored(error, "red")
