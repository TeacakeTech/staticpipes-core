class Config:

    def __init__(self, pipes: list, context: dict = {}):
        self.pipes: list = pipes
        for pipe in self.pipes:
            pipe.config = self
        self.context: dict = context
