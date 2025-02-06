class Config:

    def __init__(self, pipelines: list, context: dict = {}):
        self.pipelines: list = pipelines
        for pipeline in self.pipelines:
            pipeline.config = self
        self.context: dict = context
