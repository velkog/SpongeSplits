from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from python.runfiles import Runfiles


class ILanguage(ABC):
    @staticmethod
    @abstractmethod
    def assoc_files() -> set[str]:
        """
        A property that should return a list of valid files for this language.
        """
        pass

    @staticmethod
    @abstractmethod
    def formatter_directory() -> Path:
        """
        A property that should return the path to the directory where formatters are stored.
        """
        pass

    @classmethod
    @abstractmethod
    def formatter_cmd(cls, file: Path, in_place: bool) -> List[str]:
        """
        A property that should return the list arguments passed to the formatter.
        """
        pass


class CPP(ILanguage):
    @staticmethod
    def assoc_files() -> set[str]:
        return {
            "*.c",
            "*.c++",
            "*.cc",
            "*.cpp",
            "*.cxx",
            "*.h",
            "*.h++",
            "*.hh",
            "*.hpp",
            "*.hxx",
        }

    @staticmethod
    def formatter_directory() -> Path:
        relative_path = "llvm_tools/bin/clang-format.exe"
        r = Runfiles.Create()
        runfile_location = r.Rlocation(relative_path)
        assert runfile_location and Path(runfile_location).exists()
        return runfile_location

    @classmethod
    def formatter_cmd(cls, file: Path, in_place: bool) -> List[str]:
        cmd = [cls.formatter_directory(), str(file)]
        if in_place:
            cmd.append("-i")
        return cmd


class Python(ILanguage):
    @staticmethod
    def assoc_files() -> set[str]:
        return {
            "*.py",
            "BUILD",
            "BUILD.*",
            "*.bzl",
            "*.bazel",
        }

    @staticmethod
    def formatter_directory() -> Path:
        relative_path = "ruff/ruff.exe"
        r = Runfiles.Create()
        runfile_location = r.Rlocation(relative_path)
        assert runfile_location and Path(runfile_location).exists()
        return runfile_location

    @classmethod
    def formatter_cmd(cls, file: Path, in_place: bool) -> List[str]:
        cmds = [cls.formatter_directory(), "format", str(file)]
        if not in_place:
            cmds.append("--diff")
        return cmds


ALL_LANGUAGES = [CPP, Python]
