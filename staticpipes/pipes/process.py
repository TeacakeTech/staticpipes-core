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

    """

    def __init__(self, extensions=None, processors=None, directories: list = ["/"]):
        self.extensions: list = extensions or []
        self.processors = processors
        self.directories: list = directories

    def start_prepare(self, current_info: CurrentInfo) -> None:
        """"""
        for processor in self.processors:
            processor.config = self.config
            processor.source_directory = self.source_directory
            processor.build_directory = self.build_directory

    def prepare_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        """"""
        self._file(dir, filename, current_info, prepare=True)

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        """"""
        self._file(dir, filename, current_info, build=True)

    def _file(
        self,
        dir: str,
        filename: str,
        current_info: CurrentInfo,
        prepare: bool = False,
        build: bool = False,
    ) -> None:
        # Check Extensions
        if self.extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        # Directories
        if not staticpipes.utils.is_directory_in_list(dir, self.directories):
            return

        # TODO get as string or byte?
        process_current_info = ProcessCurrentInfo(
            dir,
            filename,
            self.source_directory.get_contents_as_str(dir, filename),
            prepare=prepare,
            build=build,
            context=current_info.get_context().copy(),
        )

        # TODO something about excluding files
        for processor in self.processors:
            processor.process_file(dir, filename, process_current_info, current_info)

        if build:
            self.build_directory.write(
                process_current_info.dir,
                process_current_info.filename,
                process_current_info.contents,
            )

    def file_changed_during_watch(self, dir, filename, current_info):
        self.build_file(dir, filename, current_info)
