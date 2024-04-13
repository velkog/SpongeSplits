from termcolor import colored, cprint

def print_error(error: str, use_colors: bool = True) -> None:
    if use_colors:
        error = colored(error, "red")
    print(f"{error}")
