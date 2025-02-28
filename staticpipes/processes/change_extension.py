from staticpipes.pipes.process import BaseProcessor


class ProcessChangeExtension(BaseProcessor):

    def __init__(self, new_extension):
        self._new_extension = new_extension

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

        filename_bits = process_current_info.filename.split(".")
        filename_bits.pop()

        new_filename = ".".join(filename_bits) + "." + self._new_extension

        process_current_info.filename = new_filename
