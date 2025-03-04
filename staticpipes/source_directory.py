import os
from contextlib import contextmanager


class SourceDirectory:

    def __init__(self, dir: str):
        self.dir = dir

    @contextmanager
    def get_contents_as_filepointer(self, dir, filename, mode=""):
        if dir != "/":
            f = os.path.join(self.dir, dir, filename)
        else:
            f = os.path.join(self.dir, filename)
        fp = open(f, "r" + mode)
        yield fp
        fp.close()

    def get_contents_as_bytes(self, dir, filename) -> bytes:
        with self.get_contents_as_filepointer(dir, filename, "b") as fp:
            return fp.read()

    def get_contents_as_str(self, dir, filename) -> str:
        with self.get_contents_as_filepointer(dir, filename, "") as fp:
            return fp.read()
