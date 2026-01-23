from .pipe_and_group_of_pipes import BasePipeAndGroupOfPipes


class BaseBundle(BasePipeAndGroupOfPipes):

    def __init__(
        self,
    ):
        super().__init__()
        self._pipes: list = None
        self._secondary_source_directory_paths = {}
        self._get_pipes_has_been_called_before: bool = False

    def get_pipes(self) -> list:
        """"""
        if not self._get_pipes_has_been_called_before:
            for pipe in self._pipes:
                pipe.config = self.config
                pipe.source_directory = self.source_directory
                pipe.secondary_source_directories = self.secondary_source_directories
                pipe.build_directory = self.build_directory
            self._get_pipes_has_been_called_before = True
        return self._pipes

    def get_secondary_source_directory_paths(self) -> dict:
        """"""
        return self._secondary_source_directory_paths
