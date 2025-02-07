import staticpipes.rjmin.rjsmin
from staticpipes.pipes.process import BaseProcessor


class ProcessJavascriptMinifier(BaseProcessor):
    """Minifies JS."""

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

        f = staticpipes.rjmin.rjsmin._make_jsmin(python_only=True)

        process_current_info.contents = f(process_current_info.contents)
