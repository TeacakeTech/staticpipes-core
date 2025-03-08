from .build_directory import BuildDirectory
from .config import Config
from .current_info import CurrentInfo
from .exceptions import WatchFunctionalityNotImplementedException
from .source_directory import SourceDirectory


class BasePipe:

    def __init__(self):
        self.config: Config = None  # type: ignore
        self.source_directory: SourceDirectory = None  # type: ignore
        self.build_directory: BuildDirectory = None  # type: ignore

    def start_prepare(self, current_info: CurrentInfo) -> None:
        """Called as we start the prepare stage."""
        pass

    def prepare_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        """Called once for every file in the prepare stage."""
        pass

    def end_prepare(self, current_info: CurrentInfo) -> None:
        """Called as we end the prepare stage."""
        pass

    def start_build(self, current_info: CurrentInfo) -> None:
        """Called as we start the build stage."""
        pass

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        """Called once for every file in the build stage,
        unless an earlier pipeline has excluded this file."""
        pass

    def file_excluded_during_build(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """Called once for every file in the build stage
        if an earlier pipeline has excluded this file."""
        pass

    def end_build(self, current_info: CurrentInfo) -> None:
        """Called as we end the build stage."""
        pass

    def start_watch(self, current_info: CurrentInfo) -> None:
        """Called as we start the prepare stage.
        There is no end_watch because the watch stage ends
        by the user stopping the whole program
        """
        pass

    def file_changed_during_watch(self, dir, filename, current_info):
        """Called once for every file as it changes during the watch stage,
        unless an earlier pipeline has excluded this file."""
        raise WatchFunctionalityNotImplementedException("Watch not implemented")

    def file_changed_but_excluded_during_watch(self, dir, filename, current_info):
        """Called once for every file as it changes during the watch stage,
        if an earlier pipeline has excluded this file."""
        pass

    def context_changed_during_watch(
        self, current_info: CurrentInfo, old_version: int, new_version: int
    ) -> None:
        """Called if the context has changed during watch."""
        pass
