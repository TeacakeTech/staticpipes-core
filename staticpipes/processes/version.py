import hashlib

import staticpipes.utils
from staticpipes.pipes.copy_with_versioning import (
    VersioningMode,
    VersioningModeInFileName,
    VersioningModeInGetParameter,
)
from staticpipes.process_base import BaseProcessor


class ProcessVersion(BaseProcessor):
    """Renames the file based on a hash of the contents,
    thus allowing them to be versioned.

    The new filename is put in the context so later pipes
    (eg Jinja2 templates) can use it.

    This should be the last process in the list of processes -
    if any processes change the filename aferwards the value
    in the context will be wrong.

    Pass:

    - context_key - the key in the context that
    new filenames will be stored in

    - versioning_mode - one of VersioningModeInGetParameter() (the default)
    or VersioningModeInFileName(). See pipes.copy_with_versioning for more information.
    """

    def __init__(
        self,
        context_key="versioning_new_filenames",
        versioning_mode: VersioningMode | None = None,
    ):
        self._context_key = context_key
        self._versioning_mode: VersioningMode = (
            versioning_mode or VersioningModeInGetParameter()
        )

    def process_source_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):
        """"""

        contents_bytes = (
            process_current_info.contents
            if isinstance(process_current_info.contents, bytes)
            else process_current_info.contents.encode("utf-8")
        )
        contents_hash = hashlib.md5(contents_bytes).hexdigest()

        if isinstance(self._versioning_mode, VersioningModeInFileName):
            filename_bits = process_current_info.filename.split(".")
            filename_extension = filename_bits.pop()
            new_filename = (
                ".".join(filename_bits) + "." + contents_hash + "." + filename_extension
            )
            new_filename_append = ""
        else:
            new_filename = source_filename
            new_filename_append = "?version=" + contents_hash

        current_info.set_context(
            [
                self._context_key,
                staticpipes.utils.make_path_from_dir_and_filename(
                    process_current_info.dir, process_current_info.filename
                ),
            ],
            staticpipes.utils.make_path_from_dir_and_filename(
                process_current_info.dir, new_filename
            )
            + new_filename_append,
        )

        process_current_info.filename = new_filename
