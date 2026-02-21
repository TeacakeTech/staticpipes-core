class Config:

    def __init__(
        self,
        pipes_and_groups_of_pipes: list | None = None,
        context: dict = {},
        checks: list = [],
    ):
        # Pipes
        self._pipes_and_groups_of_pipes: list = pipes_and_groups_of_pipes or []
        # Context
        self.context: dict = context
        # Checks
        self.checks: list = checks

    def get_pipes_and_groups_of_pipes(self) -> list:
        return self._pipes_and_groups_of_pipes
