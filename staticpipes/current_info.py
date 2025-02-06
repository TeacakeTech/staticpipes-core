class CurrentInfo:

    def __init__(self, context: dict = {}, watch: bool = False):
        self.context: dict = context
        self.watch: bool = watch
        self.current_file_excluded: bool = False

    def reset_for_new_file(self):
        self.current_file_excluded = False
