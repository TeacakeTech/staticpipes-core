class ProcessCurrentInfo:

    def __init__(self, dir: str, filename: str, contents, context: dict):
        self.dir: str = dir
        self.filename: str = filename
        self.contents = contents
        self.context: dict = context
