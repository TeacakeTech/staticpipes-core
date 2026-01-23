from .pipe_and_group_of_pipes import BasePipeAndGroupOfPipes


class BaseBundle(BasePipeAndGroupOfPipes):

    def __init__(
        self,
    ):
        super().__init__()
        self._pipes: list = None
        self._secondary_source_directory_paths = {}
        self._get_pipes_has_been_called_before: bool = False

    def get_pass_numbers(self) -> list:
        """Returns a list of pass numbers that this worker wants to run in.

        The pipes that come with staticpipes default to these pass numbers:
        - 100 for anything that excludes files or loads data into the context
        - 1000 for anything else
        When writing your own pipelines, you may want to copy that convention.
        (But also, all the pipes that come with staticpipes can have their
        pass numbers changed.)
        """
        return [1000]

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
