from .build_directory import BuildDirectory
from .config import Config
from .source_directory import SourceDirectory


class BasePipeAndGroupOfPipes(object):

    def __init__(self):
        self.config: Config = None  # type: ignore
        self.source_directory: SourceDirectory = None  # type: ignore
        self.secondary_source_directories: dict = None
        self.build_directory: BuildDirectory = None  # type: ignore
