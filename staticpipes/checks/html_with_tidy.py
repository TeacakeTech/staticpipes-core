import os
import re
import subprocess
import tempfile
from typing import Optional

import staticpipes.utils
from staticpipes.check_base import BaseCheck
from staticpipes.check_report import CheckReport


class CheckHtmlWithTidy(BaseCheck):
    """Uses tidy program to check HTML.
    Tidy must be installed.
    Can be done with tidy package in ubuntu and debian.
    """

    def __init__(
        self,
        extensions: Optional[list] = None,
    ):
        self._extensions: list = extensions or ["html"]

    def check_build_file(self, dir: str, filename: str) -> list:
        # Check Extensions
        if self._extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self._extensions
        ):
            return []

        # Create temp file
        fp_f, name_f = tempfile.mkstemp(prefix="staticpipes_check_html_with_tidy")
        os.close(fp_f)

        # Run
        subprocess.run(
            [
                "tidy",
                "-q",
                "-f",
                name_f,
                self._build_directory.get_full_filename(dir, filename),
            ],
            capture_output=True,
        )

        # Get results
        with open(name_f) as fp:
            results = fp.read()

        # Parse results
        out = []
        results_parse = re.compile(r"^line (\d+) column (\d+)")
        for result in results.split("\n"):
            if result:
                match = results_parse.match(result)
                if match:
                    line: int = int(match[1])  # type: ignore
                    column: int = int(match[2])  # type: ignore
                    out.append(
                        CheckReport(
                            type="html_with_tidy",
                            dir=dir,
                            file=filename,
                            message=result,
                            from_check=self,
                            line=line,
                            column=column,
                        )
                    )

        # Remove temp file
        os.remove(name_f)

        # Return
        return out
