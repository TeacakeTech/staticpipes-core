from .build_directory import BuildDirectory
from .config import Config
from .pipe_and_group_of_pipes_base import BasePipeAndGroupOfPipes
from .source_directory import SourceDirectory


class BaseBundle(BasePipeAndGroupOfPipes):

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self._pipes: list = None  # type: ignore
        self._secondary_source_directory_paths: dict[str, str] = None  # type: ignore

    def setup_for_worker(
        self,
        config: Config,
        source_directory: SourceDirectory,
        secondary_source_directories: dict,
        build_directory: BuildDirectory,
    ) -> None:
        super().setup_for_worker(
            config, source_directory, secondary_source_directories, build_directory
        )
        for pipe in self._pipes:
            pipe.setup_for_worker(
                config, source_directory, secondary_source_directories, build_directory
            )

    def get_pipes(self) -> list:
        """"""
        return self._pipes

    def get_secondary_source_directory_paths(self) -> dict:
        """"""
        return self._secondary_source_directory_paths
