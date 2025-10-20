class CurrentInfo:

    def __init__(self, context: dict = {}, watch: bool = False):
        self._context: dict = context
        self.watch: bool = watch
        self.current_file_excluded: bool = False
        self._context_history: list = []
        self.pass_number = 1

    def reset_for_new_pass_for_new_file(
        self, pass_number=1, current_file_excluded=False
    ):
        self.current_file_excluded = current_file_excluded
        self.pass_number = pass_number

    def reset_for_new_pass_for_same_file(self, pass_number=1):
        self.pass_number = pass_number

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
