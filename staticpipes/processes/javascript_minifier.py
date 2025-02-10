import rjsmin

from staticpipes.pipes.process import BaseProcessor


class ProcessJavascriptMinifier(BaseProcessor):
    """Minifies JS."""

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

        process_current_info.contents = rjsmin.jsmin(process_current_info.contents)
