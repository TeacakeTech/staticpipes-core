from staticpipes.build_directory import BuildDirectory
from staticpipes.config import Config
from staticpipes.current_info import CurrentInfo
from staticpipes.process_current_info import ProcessCurrentInfo
from staticpipes.source_directory import SourceDirectory


class BaseProcessor:

    def __init__(self) -> None:
        self._config: Config = None  # type: ignore
        self._source_directory: SourceDirectory = None  # type: ignore
        self._secondary_source_directories: dict = None  # type: ignore
        self._build_directory: BuildDirectory = None  # type: ignore

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

    def process_source_file(
        self,
        source_dir: str,
        source_filename: str,
        process_current_info: ProcessCurrentInfo,
        current_info: CurrentInfo,
    ):
        pass
