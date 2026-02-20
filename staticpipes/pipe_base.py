from .current_info import CurrentInfo
from .exceptions import WatchFunctionalityNotImplementedException
from .pipe_and_group_of_pipes_base import BasePipeAndGroupOfPipes


class BasePipe(BasePipeAndGroupOfPipes):

    def __init__(self) -> None:
        super().__init__()

    def start_build(self, current_info: CurrentInfo) -> None:
        """Called as we start the build stage."""
        pass

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """Called once for every file in the build stage,
        unless an earlier pipeline has excluded this file."""
        pass

    def source_file_excluded_during_build(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """Called once for every file in the build stage
        if an earlier pipeline has excluded this file."""
        pass

    def end_build(self, current_info: CurrentInfo) -> None:
        """Called as we end the build stage."""
        pass

    def start_watch(self, current_info: CurrentInfo) -> None:
        """Called once as we start the watch stage.
        There is no end_watch because the watch stage ends
        by the user stopping the whole program
        """
        pass

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """Called once for every file as it changes during the watch stage,
        unless an earlier pipeline has excluded this file."""
        raise WatchFunctionalityNotImplementedException("Watch not implemented")

    def source_file_changed_but_excluded_during_watch(
        self, dir, filename, current_info
    ):
        """Called once for every file as it changes during the watch stage,
        if an earlier pipeline has excluded this file."""
        pass

    def context_changed_during_watch(
        self, current_info: CurrentInfo, old_version: int, new_version: int
    ) -> None:
        """Called if the context has changed during watch."""
        pass
