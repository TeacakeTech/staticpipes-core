from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeExcludeDotDirectories(BasePipe):
    """Exclude any source files in directory that start with an dot,
    and any of their children,
    from any pipes that follow this one.

    Use to exclude a git folder (.git)
    """

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:

        exclude = False

        for bit in dir.split("/"):
            if bit.startswith("."):
                exclude = True

        if exclude:
            current_info.current_file_excluded = True

    def file_changed_during_watch(self, dir, filename, current_info):
        self.build_file(dir, filename, current_info)
