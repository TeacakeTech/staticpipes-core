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
        self._context: dict = context or {}
        # Checks
        self._checks: list = checks or []

    @property
    def pipes_and_groups_of_pipes(self) -> list:
        return self._pipes_and_groups_of_pipes

    @property
    def context(self) -> dict:
        return self._context

    @property
    def checks(self) -> list:
        return self._checks
