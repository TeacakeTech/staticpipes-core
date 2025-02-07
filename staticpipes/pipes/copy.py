import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeCopy(BasePipe):
    """
    A pipline that just copies files from the source directory
    to the build site (unless already excluded).
    The simplest pipeline you can get!

    Pass:

    - extensions - a list of file extensions that will be copied
    eg ["js", "css", "html"].
    If not set, all files will be copied.

    - source_sub_directory - if your files are in a subdirectory
    pass that here.
    Any files outside that will be ignored and the subdirectory
    will not appear in the build directory.
    eg pass "assets" and "assets/main.css"
    will appear in build site as "main.css"

    """

    def __init__(self, extensions=[], source_sub_directory=None):
        self.extensions = extensions
        self.source_sub_directory = (
            "/" + source_sub_directory
            if source_sub_directory and not source_sub_directory.startswith("/")
            else source_sub_directory
        )

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        if self.extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        if self.source_sub_directory:
            test_dir = "/" + dir if not dir.startswith("/") else dir
            if not test_dir.startswith(self.source_sub_directory):
                return
            out_dir = dir[len(self.source_sub_directory) :]
        else:
            out_dir = dir

        self.build_directory.write(
            out_dir,
            filename,
            self.source_directory.get_contents_as_bytes(dir, filename),
        )

    def file_changed_during_watch(self, dir, filename, current_info):
        self.build_file(dir, filename, current_info)
