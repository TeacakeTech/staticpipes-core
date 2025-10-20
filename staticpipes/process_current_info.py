class ProcessCurrentInfo:

    def __init__(self, dir, filename, contents, context: dict):
        self.dir = dir
        self.filename = filename
        self.contents = contents
        self.context: dict = context
