import os
import pathlib
import shutil
from contextlib import contextmanager


class BuildDirectory:

    def __init__(self, dir: str):
        self.dir = dir
        self.written_files: list = []

    def prepare(self):
        os.makedirs(self.dir, exist_ok=True)

    def _get_filename_to_write(self, dir: str, name: str) -> str:
        """Also makes dirs."""
        if dir != "/":
            if dir.startswith("/"):
                dir = dir[1:]
            os.makedirs(os.path.join(self.dir, dir), exist_ok=True)
            return os.path.join(self.dir, dir, name)
        else:
            return os.path.join(self.dir, name)

    def write(self, dir: str, name: str, contents):
        with open(
            self._get_filename_to_write(dir, name),
            "wb" if isinstance(contents, bytes) else "w",
        ) as fp:
            fp.write(contents)
        self.written_files.append((dir if dir else "/", name))

    def copy_in_file(self, dir: str, name: str, source_filepath: str):
        shutil.copy(
            source_filepath,
            self._get_filename_to_write(dir, name),
            follow_symlinks=True,
        )
        self.written_files.append((dir if dir else "/", name))

    def is_equal_to_source_dir(self, directory: str) -> bool:
        return os.path.realpath(self.dir) == os.path.realpath(directory)

    def remove_all_files_we_did_not_write(self):
        rpsd = os.path.realpath(self.dir)
        for root, dirs, files in os.walk(rpsd):
            for file in files:
                relative_dir = root[len(rpsd) + 1 :]
                if not relative_dir:
                    relative_dir = "/"
                if not (relative_dir, file) in self.written_files:
                    if relative_dir and relative_dir != "/":
                        pathlib.Path(
                            os.path.join(self.dir, relative_dir, file)
                        ).unlink()
                    else:
                        pathlib.Path(os.path.join(self.dir, file)).unlink()

    def get_full_filename(self, dir: str, filename: str) -> str:
        if dir != "/":
            return os.path.join(self.dir, dir, filename)
        else:
            return os.path.join(self.dir, filename)

    @contextmanager
    def get_contents_as_filepointer(self, dir, filename, mode=""):
        fp = open(self.get_full_filename(dir, filename), "r" + mode)
        yield fp
        fp.close()

    def get_contents_as_bytes(self, dir, filename) -> bytes:
        with self.get_contents_as_filepointer(dir, filename, "b") as fp:
            return fp.read()

    def get_contents_as_str(self, dir, filename) -> str:
        with self.get_contents_as_filepointer(dir, filename, "") as fp:
            return fp.read()

    def has_file(self, dir, filename) -> bool:
        return os.path.exists(self.get_full_filename(dir, filename))
