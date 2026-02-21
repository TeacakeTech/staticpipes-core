class Config:

    def __init__(
        self,
        pipes_and_groups_of_pipes: list | None = None,
        context: dict = {},
        checks: list = [],
    ):
        # Pipes
        self._pipes_and_groups_of_pipes: list = pipes_and_groups_of_pipes or []
        for pipe in self._pipes_and_groups_of_pipes:
            pipe.config = self
        # Context
        self.context: dict = context
        # Checks
        self.checks: list = checks
        for check in checks:
            check.config = self

    def get_pipes_and_groups_of_pipes(self) -> list:
        return self._pipes_and_groups_of_pipes
