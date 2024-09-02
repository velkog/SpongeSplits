from difflib import unified_diff
from pathlib import Path
from typing import Generator, List, Optional
from os import environ

class File:
    errs: Optional[List[str]] = None
    is_linted: bool = False
    reformatted: Optional[List[str]] = None

    def __init__(self, file_path: Path) -> None:
        assert file_path.exists(), f"File '{file_path}' does not exist"
        self.file_path = file_path

        with open(self.file_path, "r", encoding="utf-8") as f:
            self.original_contents = f.readlines()

    def __str__(self):
        return str(self.file_path)

    def diff(self, reformatted: List[str]) -> Generator[str, None, None]:
        relative_path = self.file_path.relative_to(environ["BUILD_WORKING_DIRECTORY"])
        return unified_diff(
            self.original_contents,
            reformatted,
            fromfile=f"{relative_path}\toriginal",
            tofile=f"{relative_path}\treformatted",
        )
