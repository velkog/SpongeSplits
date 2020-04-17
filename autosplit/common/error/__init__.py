from typing import Union

from sys import exit
from sys import stderr


def report(report: Union[str, Exception]):
    stderr.write(str(report))


def report_and_exit(report: Union[str, Exception]):
    stderr.write(str(report))
    exit(1)
