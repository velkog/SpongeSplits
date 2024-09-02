from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

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
        return "llvm_tools/bin/clang-format.exe"
