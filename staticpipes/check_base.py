from .build_directory import BuildDirectory
from .config import Config


class BaseCheck:

    def __init__(self) -> None:
        self.config: Config = None  # type: ignore
        self.build_directory: BuildDirectory = None  # type: ignore

    def start_check(self) -> list:
        """Called as we start the check stage."""
        return []

    def check_build_file(self, dir: str, filename: str) -> list:
        """Called once for every file in the check stage."""
        return []

    def end_check(self) -> list:
        """Called as we end the check stage."""
        return []
