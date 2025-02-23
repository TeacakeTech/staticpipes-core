import mako.lookup
import mako.template

import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeMako(BasePipe):

    def __init__(self, extensions=["html"]):
        self.extensions = extensions
        self.mako_lookup = None
        # This is a dumb way to process dependent templates -
        # it stores a list of all templates,
        # then in watch mode it just rebuilds ALL of them.
        self._all_templates = []

    def start_build(self, current_info: CurrentInfo) -> None:
        self.mako_lookup = mako.lookup.TemplateLookup(
            directories=[self.source_directory.dir],
            # Have to set this to zero, otherwise tests fail!!!!!!!!!
            collection_size=0,
        )

    def _actually_build_template(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:

        # print("MAKO {} {}".format(dir, filename))
        template = mako.template.Template(
            self.source_directory.get_contents_as_str(dir, filename),
            lookup=self.mako_lookup,
        )
        contents = template.render(**current_info.context)
        self.build_directory.write(dir, filename, contents)

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        self._actually_build_template(dir, filename, current_info)

        if current_info.watch:
            self._all_templates.append((dir, filename))

    def file_changed_during_watch(self, dir, filename, current_info):
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        for x in self._all_templates:
            self._actually_build_template(x[0], x[1], current_info)

    def file_changed_but_excluded_during_watch(self, dir, filename, current_info):
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        # If it has the right extension, we still reprocess all templates.
        # This is because it may be a library template file like "_layouts/index.html"
        # that an earlier pipeline excluded.
        for x in self._all_templates:
            self._actually_build_template(x[0], x[1], current_info)
