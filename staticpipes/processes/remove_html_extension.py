from staticpipes.process_base import BaseProcessor


class ProcessRemoveHTMLExtension(BaseProcessor):
    """
    Removes the HTML extension from URLs.

    It does this by putting the file in a directory and renaming it to index.html.

    eg. about.html becomes about/index.html
    """

    def process_source_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):
        """"""
        if process_current_info.filename != "index.html":
            filename_bits = process_current_info.filename.split(".")
            if filename_bits[-1] == "html":
                filename_bits.pop()
                process_current_info.dir = (
                    process_current_info.dir + "/" + ".".join(filename_bits)
                )
                process_current_info.filename = "index.html"
