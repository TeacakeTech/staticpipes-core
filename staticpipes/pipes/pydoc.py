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
        processors: list,
        pkgutil_walk_packages_args: list = [],
        module_names: list = [],
        output_dir="",
        output_filename_extension="html",
    ):
        self._pkgutil_walk_packages_args = pkgutil_walk_packages_args
        self._module_names = module_names
        self._processors = processors
        self._output_dir = output_dir
        self._output_filename_extension = output_filename_extension
        self._our_html_doc = OurHTMLDoc()

    def start_prepare(self, current_info: CurrentInfo) -> None:
        for processor in self._processors:
            processor.config = self.config
            processor.source_directory = self.source_directory
            processor.build_directory = self.build_directory

    def _build(self, current_info: CurrentInfo):
        for a1, a2 in self._pkgutil_walk_packages_args:
            for importer, modname, ispkg in pkgutil.walk_packages(a1, a2):
                self._build_modname(modname, current_info)
        for modname in self._module_names:
            self._build_modname(modname, current_info)

    def _build_modname(self, modname, current_info: CurrentInfo):

        logger.debug("Building for " + modname)
        object, name = pydoc.resolve(modname)  # type: ignore

        process_current_info = ProcessCurrentInfo(
            self._output_dir,
            name + "." + self._output_filename_extension,
            self._our_html_doc.document(object, name),
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


class OurHTMLDoc(pydoc.HTMLDoc):

    def modulelink(self, object):
        """This is ususally to a page that is not rendered,
        for now just remove hyperlink."""
        return object.__name__
