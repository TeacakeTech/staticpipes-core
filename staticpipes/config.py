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

    def get_pass_numbers(self) -> list:
        pass_numbers = []
        for pipeline in self.pipes:
            pass_numbers.extend(pipeline.get_pass_numbers())
        return sorted(list(set(pass_numbers)))

    def get_pipes_in_pass(self, pass_number: int):
        return [p for p in self.pipes if pass_number in p.get_pass_numbers()]
