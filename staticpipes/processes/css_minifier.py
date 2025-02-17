import rcssmin

from staticpipes.pipes.process import BaseProcessor


class ProcessCSSMinifier(BaseProcessor):
    """Minifies CSS."""

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

        process_current_info.contents = rcssmin.cssmin(process_current_info.contents)
