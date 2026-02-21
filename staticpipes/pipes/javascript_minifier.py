import rjsmin

import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeJavascriptMinifier(BasePipe):
    """
    A pipline that copies JS files from the source directory
    to the build site (unless already excluded)
    and minifies them at the same time.
    """

    def __init__(self, extensions: list[str] | None = None):
        self._extensions: list[str] = extensions or ["js"]

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""
        if self._extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self._extensions
        ):
            return

        self._build_directory.write(
            dir,
            filename,
            rjsmin.jsmin(self._source_directory.get_contents_as_str(dir, filename)),
        )

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """"""
        self.build_source_file(dir, filename, current_info)

    def get_description_for_logs(self) -> str:
        """"""
        return "Javascript Minifier (Extensions {})".format(self._extensions)
