from staticpipes.check_base import BaseCheck
from staticpipes.check_report import CheckReport


class CheckFileContainsText(BaseCheck):
    """Checks that a given output file has some text in."""

    def __init__(self, directory: str, filename: str, text: str):
        self._directory: str = directory
        self._filename: str = filename
        self._text: str = text

    def end_check(self) -> list:
        if not self._build_directory.has_file(self._directory, self._filename):
            return [
                CheckReport(
                    dir=self._directory,
                    file=self._filename,
                    message="File is missing",
                    type="file_contains_text_missing_file",
                    from_check=self,
                )
            ]

        # TODO double check it is a file and not a directory

        contents = self._build_directory.get_contents_as_str(
            self._directory, self._filename
        )
        if self._text not in contents:
            return [
                CheckReport(
                    dir=self._directory,
                    file=self._filename,
                    message="File Does not contain text: {}".format(self._text),
                    type="file_contains_text_missing_text",
                    from_check=self,
                )
            ]

        return []
