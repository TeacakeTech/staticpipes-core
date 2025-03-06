from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe
from staticpipes.process_current_info import ProcessCurrentInfo


class PipeCollectionItemsProcess(BasePipe):

    def __init__(
        self,
        type_id: str,
        processors: list,
        output_dir=None,
        output_filename_extension="html",
    ):
        self._type_id = type_id
        self._processors = processors
        self._output_dir = output_dir or type_id
        self._output_filename_extension = output_filename_extension

    def start_prepare(self, current_info: CurrentInfo) -> None:
        for processor in self._processors:
            processor.config = self.config
            processor.source_directory = self.source_directory
            processor.build_directory = self.build_directory

    def _build(self, current_info: CurrentInfo):

        collection = current_info.get_context("collection")[self._type_id]

        for item in collection.get_items():
            this_context = current_info.get_context().copy()
            this_context["item_id"] = item.get_id()
            this_context["item_data"] = item.get_data()

            process_current_info = ProcessCurrentInfo(
                self._output_dir,
                item.get_id() + "." + self._output_filename_extension,
                "",
                prepare=False,
                build=True,
                context=this_context,
            )

            # TODO something about excluding files
            for processor in self._processors:
                processor.process_file(
                    self._output_dir,
                    item.get_id() + "." + self._output_filename_extension,
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
