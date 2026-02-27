from staticpipes.check_base import BaseCheck
from staticpipes.check_report import CheckReport

DEFAULT_CHECK_HTML_TAG_SETTINGS = {"img": {"required_attributes": ["alt"]}}


class CheckFileExists(BaseCheck):
    """Checks that a given output file exists."""

    def __init__(self, directory: str, filename: str):
        self._directory: str = directory
        self._filename: str = filename

    def end_check(self) -> list:
        if not self._build_directory.has_file(self._directory, self._filename):
            return [
                CheckReport(
                    dir=self._directory,
                    file=self._filename,
                    message="File is missing",
                    type="file_exists_missing_file",
                    from_check=self,
                )
            ]

        # TODO double check it is a file and not a directory

        return []
