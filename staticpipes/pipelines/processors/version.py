import hashlib

from staticpipes.pipelines.process import BaseProcessor


class ProcessVersion(BaseProcessor):
    """Renames the file based on a hash of the contents,
    thus allowing them to be versioned.

    The new filename is put in the context so later pipelines
    (eg Jinja2 templates) can use it.
    """

    def __init__(
        self,
        context_key="versioning_new_filenames",
    ):
        self.context_key = context_key

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):

        contents_bytes = (
            process_current_info.contents
            if isinstance(process_current_info.contents, bytes)
            else process_current_info.contents.encode("utf-8")
        )
        hash = hashlib.md5(contents_bytes).hexdigest()
        filename_bits = process_current_info.filename.split(".")
        filename_extension = filename_bits.pop()

        new_filename = ".".join(filename_bits) + "." + hash + "." + filename_extension

        if self.context_key not in current_info.context:
            current_info.context[self.context_key] = {}

        key = (
            (
                ""
                if process_current_info.dir == "" or process_current_info.dir == "/"
                else (
                    process_current_info.dir
                    if process_current_info.dir.startswith("/")
                    else "/" + process_current_info.dir
                )
            )
            + "/"
            + process_current_info.filename
        )
        value = (
            (
                ""
                if process_current_info.dir == "" or process_current_info.dir == "/"
                else (
                    process_current_info.dir
                    if process_current_info.dir.startswith("/")
                    else "/" + process_current_info.dir
                )
            )
            + "/"
            + new_filename
        )
        current_info.context[self.context_key][key] = value

        process_current_info.filename = new_filename
