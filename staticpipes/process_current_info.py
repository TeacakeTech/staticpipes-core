class ProcessCurrentInfo:

    def __init__(self, dir: str, filename: str, contents, context: dict):
        self._dir: str = dir
        self._filename: str = filename
        self._contents = contents
        self._context: dict = context

    @property
    def dir(self) -> str:
        return self._dir

    @dir.setter
    def dir(self, dir: str):
        self._dir = dir

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        self._filename = filename

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, contents):
        self._contents = contents

    @property
    def context(self) -> dict:
        return self._context

    def set_context(self, key, value):
        if isinstance(key, str):
            self._context[key] = value
        else:
            s = self._context
            while len(key) > 1:
                bit = key.pop(0)
                if bit not in s:
                    s[bit] = {}
                s = s[bit]
            s[key[0]] = value
