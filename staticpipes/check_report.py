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
        self._type: str = type
        self._dir: str = dir
        self._file: str = file
        self._message: str = message
        self._generator_class: str = from_check.__class__.__name__
        self._line: Optional[int] = line
        self._column: Optional[int] = column

    def json(self):
        return {
            "type": self._type,
            "dir": self._dir,
            "file": self._file,
            "message": self._message,
            "generator": {"class": self._generator_class},
            "line": self._line,
            "column": self._column,
        }

    def get_description_for_logs(self) -> str:
        return (
            "Report: \n"
            + "  type      : {} from generator {}\n".format(
                self._type, self._generator_class
            )
            + "  dir       : {}\n".format(self._dir)
            + "  file      : {}\n".format(self._file)
            + "  message   : {}\n".format(self._message)
            + "  line, col : {}, {}".format(self._line, self._column)
        )
