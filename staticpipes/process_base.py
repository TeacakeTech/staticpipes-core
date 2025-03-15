from staticpipes.build_directory import BuildDirectory
from staticpipes.config import Config
from staticpipes.current_info import CurrentInfo
from staticpipes.process_current_info import ProcessCurrentInfo
from staticpipes.source_directory import SourceDirectory


class BaseProcessor:

    def __init__(self):
        self.config: Config = None  # type: ignore
        self.source_directory: SourceDirectory = None  # type: ignore
        self.build_directory: BuildDirectory = None  # type: ignore

    def process_file(
        self,
        source_dir: str,
        source_filename: str,
        process_current_info: ProcessCurrentInfo,
        current_info: CurrentInfo,
    ):
        pass
