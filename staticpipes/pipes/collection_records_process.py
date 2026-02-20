from collections.abc import Callable
from typing import Optional

from staticpipes.collection_base import BaseCollectionRecord
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe
from staticpipes.process_current_info import ProcessCurrentInfo


class PipeCollectionRecordsProcess(BasePipe):
    """
    Takes a collection, and for every item in that collection
    passes it throught a series of processes you define.

    Typical uses include with the Jinja2 process, so you can make
    a HTML page for every item in a collection.

    Pass:

    - collection_name

    - processors

    - output_mode. Should be one of "file" (default) or "dir".
    In "file" mode, the output file for each record is
    "output_dir/id.output_filename_extension".
    In "dir" mode, it's "output_dir/id/output_filename"

    - output_dir

    - output_filename_extension

    - output_filename

    - context_key_record_id

    - context_key_record_data

    - context_key_record_class

    - filter_function


    """

    def __init__(
        self,
        collection_name: str,
        processors: list,
        output_mode: str = "file",
        output_dir=None,
        output_filename_extension="html",
        output_filename="index.html",
        context_key_record_id: str = "record_id",
        context_key_record_data: str = "record_data",
        context_key_record_class: str = "record",
        filter_function: Optional[Callable[[BaseCollectionRecord], bool]] = None,
    ):
        self._collection_name = collection_name
        self._processors = processors
        self._output_mode = output_mode
        self._output_dir = output_dir or collection_name
        self._output_filename_extension = output_filename_extension
        self._output_filename = output_filename
        self._context_key_record_id = context_key_record_id
        self._context_key_record_data = context_key_record_data
        self._context_key_record_class = context_key_record_class
        self._filter_function: Optional[Callable[[BaseCollectionRecord], bool]] = (
            filter_function
        )

    def start_build(self, current_info: CurrentInfo) -> None:
        """"""
        for processor in self._processors:
            processor.config = self.config
            processor.source_directory = self.source_directory
            processor.build_directory = self.build_directory

        collection = current_info.get_context("collection")[self._collection_name]

        for record in collection.get_records():

            if self._filter_function and not self._filter_function(record):
                continue

            this_context = current_info.get_context().copy()
            this_context[self._context_key_record_id] = record.get_id()
            this_context[self._context_key_record_data] = record.get_data()
            this_context[self._context_key_record_class] = record

            if self._output_mode == "file":
                new_dir = self._output_dir
                new_filename = record.get_id() + "." + self._output_filename_extension
            elif self._output_mode == "dir":
                new_dir = self._output_dir + "/" + record.get_id()
                new_filename = self._output_filename
            else:
                raise Exception("Unrecognised output mode")

            process_current_info = ProcessCurrentInfo(
                new_dir,
                new_filename,
                "",
                context=this_context,
            )

            # TODO something about excluding files
            for processor in self._processors:
                processor.process_source_file(
                    self._output_dir,
                    record.get_id() + "." + self._output_filename_extension,
                    process_current_info,
                    current_info,
                )

            self.build_directory.write(
                process_current_info.dir,
                process_current_info.filename,
                process_current_info.contents,
            )
