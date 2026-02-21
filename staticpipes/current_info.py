class CurrentInfo:

    def __init__(self, context: dict = {}, watch: bool = False):
        self._context: dict = context
        self._watch: bool = watch
        self._current_file_excluded: bool = False
        self._context_history: list = []

    @property
    def watch(self) -> bool:
        return self._watch

    @property
    def current_file_excluded(self) -> bool:
        return self._current_file_excluded

    @current_file_excluded.setter
    def current_file_excluded(self, current_file_excluded: bool):
        self._current_file_excluded = current_file_excluded

    def set_current_file_excluded(self, current_file_excluded: bool):
        """deprecated. Can set directly now."""
        self._current_file_excluded = current_file_excluded

    def get_context(self, key=None):
        if isinstance(key, str):
            return self._context[key]
        else:
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
        if self.watch:
            self._context_history.append(key)

    def get_context_version(self) -> int:
        if self.watch:
            return len(self._context_history)
        else:
            raise Exception("This only works in watch mode")
