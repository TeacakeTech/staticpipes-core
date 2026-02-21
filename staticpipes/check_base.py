from .build_directory import BuildDirectory
from .config import Config


class BaseCheck:

    def __init__(self) -> None:
        self._config: Config = None  # type: ignore
        self._build_directory: BuildDirectory = None  # type: ignore

    def setup_for_worker(
        self,
        config: Config,
        build_directory: BuildDirectory,
    ) -> None:
        self._config = config
        self._build_directory = build_directory

    def start_check(self) -> list:
        """Called as we start the check stage."""
        return []

    def check_build_file(self, dir: str, filename: str) -> list:
        """Called once for every file in the check stage."""
        return []

    def end_check(self) -> list:
        """Called as we end the check stage."""
        return []
