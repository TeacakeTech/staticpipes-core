import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeCopy(BasePipe):
    """
    A pipeline that just copies files from the source directory
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

    - directories - Only items in these directories and
    their children will be copied.

    """

    def __init__(
        self,
        extensions=None,
        source_sub_directory=None,
        directories: list = ["/"],
    ):
        self._extensions: list = extensions or []
        self._source_sub_directory = (
            "/" + source_sub_directory
            if source_sub_directory and not source_sub_directory.startswith("/")
            else source_sub_directory
        )
        self._directories: list = directories

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""
        # Check Extensions
        if self._extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self._extensions
        ):
            return

        # Directories
        if not staticpipes.utils.is_directory_in_list(dir, self._directories):
            return

        # Source Sub Dir then copy
        if self._source_sub_directory:
            test_dir = "/" + dir if not dir.startswith("/") else dir
            if not test_dir.startswith(self._source_sub_directory):
                return
            out_dir = dir[len(self._source_sub_directory) :]
        else:
            out_dir = dir

        self.build_directory.copy_in_file(
            out_dir,
            filename,
            self.source_directory.get_full_filename(dir, filename),
        )

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """"""
        self.build_source_file(dir, filename, current_info)

    def get_description_for_logs(self) -> str:
        """"""
        return "Copy (Extensions {}, Source Subdirectory {}, Directories {})".format(
            self._extensions, self._source_sub_directory, self._directories
        )
