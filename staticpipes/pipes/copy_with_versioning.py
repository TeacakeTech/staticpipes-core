import abc
import hashlib

import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class VersioningMode(abc.ABC):
    """Abstract class, every versioning mode should inherit from this class."""

    pass


class VersioningModeInGetParameter(VersioningMode):
    """
    The version information is put in the get parameter.

    eg /js/main.js becomes /js/main.js?version=ceba641cf86025b52dfc12a1b847b4d8

    This way, if a client somehow has an older link
    (eg /js/main.js?version=73229b70fe5f1ad4bf6e6ef249287ad4 )
    the file will still load and not be a 404.
    The client may have an older link because:
    * A new version is deployed in the middle of loading contents.
    * The old link is cached somewhere, maybe the HTML could be cached.
    * The old link is used on an external website, say a social media preview image.
    """

    pass


class VersioningModeInFileName(VersioningMode):
    """
    The version information is put in the filename.

    eg /js/main.js becomes /js/main.b1cee5ed8ca8405563a5be2227ddab36.js

    This way, if a client somehow has an older link
    (eg /js/main.73229b70fe5f1ad4bf6e6ef249287ad4.js )
    they will get a 404.
    """

    pass


class PipeCopyWithVersioning(BasePipe):
    """
    A pipline that copies files from the source directory
    to the build site (unless already excluded) while
    renaming the file based on a hash of the contents,
    thus allowing them to be versioned.

    The new filename is put in the context so later pipes
    (eg Jinja2 templates) can use it.

    Pass:

    - extensions - a list of file extensions that will be copied
    eg ["js", "css"].
    You can pass an empty list to copy all files.

    - source_sub_directory - if your files are in a subdirectory
    pass that here.
    Any files outside that will be ignored and the subdirectory
    will not appear in the build directory.
    eg pass "assets" and "assets/main.css"
    will appear in build site as "main.css"

    - context_key - the key in the context that
    new filenames will be stored in

    - directories - Only items in these directories and
    their children will be copied.

    - versioning_mode - one of VersioningModeInGetParameter() (the default)
    or VersioningModeInFileName()
    """

    def __init__(
        self,
        extensions: list[str] | None = None,
        context_key: str = "versioning_new_filenames",
        source_sub_directory=None,
        directories: list[str] | None = None,
        versioning_mode: VersioningMode | None = None,
    ):
        self._extensions: list[str] = extensions or ["js", "css"]
        self._context_key = context_key
        self._source_sub_directory = (
            "/" + source_sub_directory
            if source_sub_directory and not source_sub_directory.startswith("/")
            else source_sub_directory
        )
        self._directories: list[str] = directories or ["/"]
        self._versioning_mode: VersioningMode = (
            versioning_mode or VersioningModeInGetParameter()
        )

    def build_source_file(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        """"""
        # Check Extensions
        if self._extensions and not staticpipes.utils.does_filename_have_extension(
            filename, self._extensions
        ):
            return

        # Directories
        if not staticpipes.utils.is_directory_in_list(dir, self._directories):
            return

        # Source Sub Dir then copy
        if self._source_sub_directory:
            test_dir = "/" + dir if not dir.startswith("/") else dir
            if not test_dir.startswith(self._source_sub_directory):
                return
            out_dir = dir[len(self._source_sub_directory) :]
        else:
            out_dir = dir

        # Make new filename
        contents = self._source_directory.get_contents_as_bytes(dir, filename)
        contents_hash = hashlib.md5(contents).hexdigest()

        if isinstance(self._versioning_mode, VersioningModeInFileName):
            filename_bits = filename.split(".")
            filename_extension = filename_bits.pop()
            new_filename = (
                ".".join(filename_bits) + "." + contents_hash + "." + filename_extension
            )
            new_filename_append = ""
        else:
            new_filename = filename
            new_filename_append = "?version=" + contents_hash

        current_info.set_context(
            [
                self._context_key,
                staticpipes.utils.make_path_from_dir_and_filename(out_dir, filename),
            ],
            staticpipes.utils.make_path_from_dir_and_filename(out_dir, new_filename)
            + new_filename_append,
        )

        # Copy File
        self._build_directory.copy_in_file(
            out_dir,
            new_filename,
            self._source_directory.get_full_filename(dir, filename),
        )

    def source_file_changed_during_watch(self, dir, filename, current_info):
        """"""
        self.build_source_file(dir, filename, current_info)

    def get_description_for_logs(self) -> str:
        """"""
        return "Copy With Versioning (extensions {})".format(self._extensions)
