from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeExcludeUnderscoreDirectories(BasePipe):
    """Exclude any source files in directory that start with an underscore,
    and any of their children,
    from any pipes that follow this one.

    Use to exclude any library files eg template layouts in a "_layouts" directory.
    """

    def __init__(self, pass_number=100):
        self._pass_number: int = pass_number

    def get_pass_numbers(self) -> list:
        """"""
        return [self._pass_number]

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""

        exclude = False

        for bit in dir.split("/"):
            if bit.startswith("_"):
                exclude = True

        if exclude:
            current_info.current_file_excluded = True

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """"""
        self.build_source_file(dir, filename, current_info)
