from .build_directory import BuildDirectory
from .config import Config
from .source_directory import SourceDirectory


class BasePipeAndGroupOfPipes(object):

    def __init__(self) -> None:
        self.config: Config = None  # type: ignore
        self.source_directory: SourceDirectory = None  # type: ignore
        self.secondary_source_directories: dict = None  # type: ignore
        self.build_directory: BuildDirectory = None  # type: ignore

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
        self.config = config
        self.source_directory = source_directory
        self.secondary_source_directories = secondary_source_directories
        self.build_directory = build_directory
