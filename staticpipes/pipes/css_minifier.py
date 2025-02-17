import rcssmin

import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeCSSMinifier(BasePipe):
    """
    A pipline that copies CSS files from the source directory
    to the build site (unless already excluded)
    and minifies them at the same time.
    """

    def __init__(self, extensions=["css"]):
        self.extensions = extensions

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        if self.extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        self.build_directory.write(
            dir,
            filename,
            rcssmin.cssmin(self.source_directory.get_contents_as_str(dir, filename)),
        )

    def file_changed_during_watch(self, dir, filename, current_info):
        self.build_file(dir, filename, current_info)
