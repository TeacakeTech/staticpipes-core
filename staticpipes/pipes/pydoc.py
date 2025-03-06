import logging
import pkgutil
import pydoc

from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe
from staticpipes.process_current_info import ProcessCurrentInfo

logger = logging.getLogger(__name__)


class PipePydoc(BasePipe):

    def __init__(
        self,
        pydoc_dir,
        processors: list,
        pydoc_pkgpath="",
        output_dir="",
        output_filename_extension="html",
    ):
        self._pydoc_dir = pydoc_dir
        self._pydoc_pkgpath = pydoc_pkgpath
        self._processors = processors
        self._output_dir = output_dir
        self._output_filename_extension = output_filename_extension

    def start_prepare(self, current_info: CurrentInfo) -> None:
        for processor in self._processors:
            processor.config = self.config
            processor.source_directory = self.source_directory
            processor.build_directory = self.build_directory

    def _build(self, current_info: CurrentInfo):

        html = pydoc.HTMLDoc()

        for importer, modname, ispkg in pkgutil.walk_packages(
            [self._pydoc_dir], self._pydoc_pkgpath
        ):
            logger.debug("Building for " + modname)
            object, name = pydoc.resolve(modname)  # type: ignore

            process_current_info = ProcessCurrentInfo(
                self._output_dir,
                name + "." + self._output_filename_extension,
                html.document(object, name),
                prepare=False,
                build=True,
                context=current_info.get_context().copy(),
            )

            # TODO something about excluding files
            for processor in self._processors:
                processor.process_file(
                    self._output_dir,
                    name + "." + self._output_filename_extension,
                    process_current_info,
                    current_info,
                )

            self.build_directory.write(
                process_current_info.dir,
                process_current_info.filename,
                process_current_info.contents,
            )

    def start_build(self, current_info: CurrentInfo) -> None:
        self._build(current_info)
