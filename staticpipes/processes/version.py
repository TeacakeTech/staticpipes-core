import hashlib

import staticpipes.utils
from staticpipes.pipes.process import BaseProcessor


class ProcessVersion(BaseProcessor):
    """Renames the file based on a hash of the contents,
    thus allowing them to be versioned.

    The new filename is put in the context so later pipes
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

        current_info.set_context(
            [
                self.context_key,
                staticpipes.utils.make_path_from_dir_and_filename(
                    process_current_info.dir, process_current_info.filename
                ),
            ],
            staticpipes.utils.make_path_from_dir_and_filename(
                process_current_info.dir, new_filename
            ),
        )

        process_current_info.filename = new_filename
