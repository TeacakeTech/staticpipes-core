from staticpipes.current_info import CurrentInfo
from staticpipes.pipeline_base import BasePipeLine


class PipeLineExcludeUnderscoreDirectories(BasePipeLine):
    """Exclude any source files in directory that start with an underscore,
    and any of their children,
    from any pipelines that follow this one.

    Use to exclude any library files eg template layouts in a "_layouts" directory.
    """

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:

        exclude = False

        for bit in dir.split("/"):
            if bit.startswith("_"):
                exclude = True

        if exclude:
            current_info.current_file_excluded = True
