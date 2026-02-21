class Config:

    def __init__(
        self,
        pipes_and_groups_of_pipes: list | None = None,
        context: dict | None = None,
        checks: list | None = None,
    ):
        # Pipes
        self._pipes_and_groups_of_pipes: list = pipes_and_groups_of_pipes or []
        # Context
        self.context: dict = context or {}
        # Checks
        self.checks: list = checks or []

    def get_pipes_and_groups_of_pipes(self) -> list:
        return self._pipes_and_groups_of_pipes
