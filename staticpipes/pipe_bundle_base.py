from .current_info import CurrentInfo
from .pipe_base import BasePipe


class BasePipeBundle(BasePipe):

    def __init__(
        self,
        pass_number=1000,
    ):
        self._pass_number = pass_number
        self._pipes: list = []

    def start_build(self, current_info: CurrentInfo) -> None:
        """"""
        for pipe in self._pipes:
            pipe.config = self.config
            pipe.source_directory = self.source_directory
            pipe.secondary_source_directories = self.secondary_source_directories
            pipe.build_directory = self.build_directory
            pipe.start_build(current_info)

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""
        for pipe in self._pipes:
            pipe.build_source_file(dir, filename, current_info)

    def source_file_excluded_during_build(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""
        for pipe in self._pipes:
            pipe.source_file_excluded_during_build(dir, filename, current_info)

    def end_build(self, current_info: CurrentInfo) -> None:
        """"""
        for pipe in self._pipes:
            pipe.end_build(current_info)

    def start_watch(self, current_info: CurrentInfo) -> None:
        """"""
        for pipe in self._pipes:
            pipe.start_watch(current_info)

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """"""
        for pipe in self._pipes:
            pipe.source_file_changed_during_watch(dir, filename, current_info)

    def source_file_changed_but_excluded_during_watch(
        self, dir, filename, current_info
    ):
        """"""
        for pipe in self._pipes:
            pipe.source_file_changed_but_excluded_during_watch(
                dir, filename, current_info
            )

    def context_changed_during_watch(
        self, current_info: CurrentInfo, old_version: int, new_version: int
    ) -> None:
        """"""
        for pipe in self._pipes:
            pipe.context_changed_during_watch(current_info, old_version, new_version)
