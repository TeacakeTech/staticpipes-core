class ProcessCurrentInfo:

    def __init__(
        self, dir, filename, contents, prepare: bool, build: bool, context: dict
    ):
        self.dir = dir
        self.filename = filename
        self.contents = contents
        self.prepare: bool = prepare
        self.build: bool = build
        self.context: dict = context
