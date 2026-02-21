from .build_directory import BuildDirectory
from .config import Config
from .source_directory import SourceDirectory


class BasePipeAndGroupOfPipes(object):

    def __init__(self) -> None:
        self._config: Config = None  # type: ignore
        self._source_directory: SourceDirectory = None  # type: ignore
        self._secondary_source_directories: dict = None  # type: ignore
        self._build_directory: BuildDirectory = None  # type: ignore

    def get_description_for_logs(self) -> str:
        """Returns a string describing this pipe, for use in the logs."""
        return str(self)

    def setup_for_worker(
        self,
        config: Config,
        source_directory: SourceDirectory,
        secondary_source_directories: dict,
        build_directory: BuildDirectory,
    ) -> None:
        self._config = config
        self._source_directory = source_directory
        self._secondary_source_directories = secondary_source_directories
        self._build_directory = build_directory
