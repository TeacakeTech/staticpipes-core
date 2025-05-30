from typing import Optional

from .check_base import BaseCheck


class CheckReport:

    def __init__(
        self,
        type: str,
        dir: str,
        file: str,
        message: str,
        from_check: BaseCheck,
        line: Optional[int] = None,
        column: Optional[int] = None,
    ):
        self.type: str = type
        self.dir: str = dir
        self.file: str = file
        self.message: str = message
        self.generator_class: str = from_check.__class__.__name__
        self.line: Optional[int] = line
        self.column: Optional[int] = column

    def json(self):
        return {
            "type": self.type,
            "dir": self.dir,
            "file": self.file,
            "message": self.message,
            "generator": {"class": self.generator_class},
            "line": self.line,
            "column": self.column,
        }
