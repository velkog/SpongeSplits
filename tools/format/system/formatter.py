from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from python.runfiles import Runfiles


class IFormatter(ABC):
    @staticmethod
    @abstractmethod
    def assoc_files() -> set[str]:
        """
        A property that should return a list of valid files for this formatter.
        """
        pass

    @staticmethod
    @abstractmethod
    def formatter_directory() -> Path:
        """
        A property that should return the path to the directory where the formatter is stored.
        """
        pass

    @classmethod
    @abstractmethod
    def formatter_cmd(cls, file: Path, in_place: bool) -> List[str]:
        """
        A property that should return the command list to execute the formatter
        """
        pass


class ClangFormat(IFormatter):
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


class RuffFormat(IFormatter):
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


class RuffLint(RuffFormat):
    @staticmethod
    def assoc_files() -> set[str]:
        return {
            "*.py",
        }

    @classmethod
    def formatter_cmd(cls, file: Path, in_place: bool) -> List[str]:
        cmds = [cls.formatter_directory(), "check", str(file)]
        if in_place:
            cmds.append("--fix")
        return cmds


ALL_FORMATTERS = [ClangFormat, RuffFormat, RuffLint]
