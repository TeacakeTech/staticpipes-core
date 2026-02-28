class Config:

    def __init__(
        self,
        pipes_and_groups_of_pipes: list | None = None,
        context: dict | None = None,
        checks: list | None = None,
        remove_build_directory_content_we_did_not_touch: bool = True,
    ):
        self._pipes_and_groups_of_pipes: list = pipes_and_groups_of_pipes or []
        self._context: dict = context or {}
        self._checks: list = checks or []
        self._remove_build_directory_content_we_did_not_touch: bool = (
            remove_build_directory_content_we_did_not_touch
        )

    @property
    def pipes_and_groups_of_pipes(self) -> list:
        return self._pipes_and_groups_of_pipes

    @property
    def context(self) -> dict:
        return self._context

    @property
    def checks(self) -> list:
        return self._checks

    @property
    def remove_build_directory_content_we_did_not_touch(self) -> bool:
        return self._remove_build_directory_content_we_did_not_touch
