from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeCopyFromSecondarySource(BasePipe):
    """
    A pipeline that just copies a specified file from a secondary source directory
    to the build site.
    """

    def __init__(
        self,
        secondary_source_name: str,
        source_directory: str,
        source_filename: str,
        destination_directory: str | None = None,
        destination_filename: str | None = None,
    ):
        self._secondary_source_name: str = secondary_source_name
        self._source_directory_name: str = source_directory
        self._source_filename: str = source_filename
        self._destination_directory_name: str = (
            destination_directory or source_directory
        )
        self._destination_filename: str = destination_filename or source_filename

    def start_build(self, current_info: CurrentInfo) -> None:
        self._build_directory.copy_in_file(
            self._destination_directory_name,
            self._destination_filename,
            self._secondary_source_directories[
                self._secondary_source_name
            ].get_full_filename(self._source_directory_name, self._source_filename),
        )

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """"""
        pass

    def get_description_for_logs(self) -> str:
        """"""
        return (
            "Copy From Secondary Source "
            + "(Secondary Source {}, Source Dir {}, Source filename {}, "
            + "Destination Dir {}, Destination filename {}"
        ).format(
            self._secondary_source_name,
            self._source_directory_name,
            self._source_filename,
            self._destination_directory_name,
            self._destination_filename,
        )
