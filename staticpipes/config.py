class Config:

    def __init__(self, pipes: list = [], context: dict = {}, checks: list = []):
        # Pipes
        self.pipes: list = pipes
        for pipe in self.pipes:
            pipe.config = self
        # Context
        self.context: dict = context
        # Checks
        self.checks: list = checks
        for check in checks:
            check.config = self

    def get_pipes(self) -> list:
        return self.pipes
