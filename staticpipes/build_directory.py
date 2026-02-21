import os
import pathlib
import shutil

from .directory_base import BaseDirectory


class BuildDirectory(BaseDirectory):

    def __init__(self, dir: str):
        super().__init__(dir)
        self._written_files: list[tuple[str, str]] = []

    def prepare(self):
        os.makedirs(self._dir, exist_ok=True)

    def _written_files_append(self, dir: str, name: str):
        if dir != "/":
            while dir.startswith("/"):
                dir = dir[1:]
        self._written_files.append((dir if dir else "/", name))

    def _get_filename_to_write(self, dir: str, name: str) -> str:
        """Also makes dirs."""
        if dir != "/":
            while dir.startswith("/"):
                dir = dir[1:]
            os.makedirs(os.path.join(self._dir, dir), exist_ok=True)
            return os.path.join(self._dir, dir, name)
        else:
            return os.path.join(self._dir, name)

    def write(self, dir: str, name: str, contents):
        with open(
            self._get_filename_to_write(dir, name),
            "wb" if isinstance(contents, bytes) else "w",
        ) as fp:
            fp.write(contents)
        self._written_files_append(dir, name)

    def copy_in_file(self, dir: str, name: str, source_filepath: str):
        shutil.copy(
            source_filepath,
            self._get_filename_to_write(dir, name),
            follow_symlinks=True,
        )
        self._written_files_append(dir, name)

    def is_equal_to_source_dir(self, directory: str) -> bool:
        return os.path.realpath(self._dir) == os.path.realpath(directory)

    def remove_all_files_we_did_not_write(self):
        rpsd = os.path.realpath(self._dir)
        for root, dirs, files in os.walk(rpsd):
            for file in files:
                relative_dir = root[len(rpsd) + 1 :]
                if not relative_dir:
                    relative_dir = "/"
                if not (relative_dir, file) in self._written_files:
                    if relative_dir and relative_dir != "/":
                        pathlib.Path(
                            os.path.join(self._dir, relative_dir, file)
                        ).unlink()
                    else:
                        pathlib.Path(os.path.join(self._dir, file)).unlink()
