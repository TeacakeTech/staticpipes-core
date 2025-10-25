import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe
from staticpipes.process_current_info import ProcessCurrentInfo


class PipeProcess(BasePipe):
    """A pipeline that takes files and passes them through
    a series of processes you define.
    This allows one source file to go through multiple processes
    before being put in the build site.

    Only works on files with the right extensions not already
    excluded by earlier pipes.

    For processes, see classes in staticpipes.processes package

    Pass:

    - extensions - a list of file extensions that will be processed
    eg ["js", "css", "html"].
    If not set, all files will be processed.

    - directories - Only items in these directories and
    their children will be processed.

    - processors - a list of instances of processors from the
    staticpipes.pipes.processors package

    - binary_content - should we handle content as a binary?
    Defaults to False, in which case it's handled as a string.

    """

    def __init__(
        self,
        extensions=None,
        processors=None,
        directories: list = ["/"],
        binary_content: bool = False,
        pass_number: int = 1000,
    ):
        self.extensions: list = extensions or []
        self.processors = processors
        self.directories: list = directories
        self.binary_content: bool = binary_content
        self._pass_number: int = pass_number

    def get_pass_numbers(self) -> list:
        """"""
        return [self._pass_number]

    def start_build(self, current_info: CurrentInfo) -> None:
        """"""
        for processor in self.processors:
            processor.config = self.config
            processor.source_directory = self.source_directory
            processor.build_directory = self.build_directory

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""
        self._file(dir, filename, current_info)

    def _file(
        self,
        dir: str,
        filename: str,
        current_info: CurrentInfo,
    ) -> None:
        # Check Extensions
        if self.extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        # Directories
        if not staticpipes.utils.is_directory_in_list(dir, self.directories):
            return

        # Ok, start to process ...
        process_current_info = ProcessCurrentInfo(
            dir,
            filename,
            (
                self.source_directory.get_contents_as_bytes(dir, filename)
                if self.binary_content
                else self.source_directory.get_contents_as_str(dir, filename)
            ),
            context=current_info.get_context().copy(),
        )

        # TODO something about excluding files
        for processor in self.processors:
            processor.process_source_file(
                dir, filename, process_current_info, current_info
            )

        # Write
        self.build_directory.write(
            process_current_info.dir,
            process_current_info.filename,
            process_current_info.contents,
        )

    def source_file_changed_during_watch(self, dir, filename, current_info):
        self.build_source_file(dir, filename, current_info)
