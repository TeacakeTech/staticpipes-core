import os


class SourceDirectory:

    def __init__(self, dir: str):
        self.dir = dir

    def get_contents_as_bytes(self, dir, filename) -> bytes:
        if dir != "/":
            f = os.path.join(self.dir, dir, filename)
        else:
            f = os.path.join(self.dir, filename)
        with open(f, "rb") as fp:
            return fp.read()

    def get_contents_as_str(self, dir, filename) -> str:
        if dir != "/":
            f = os.path.join(self.dir, dir, filename)
        else:
            f = os.path.join(self.dir, filename)
        with open(f, "r") as fp:
            return fp.read()
