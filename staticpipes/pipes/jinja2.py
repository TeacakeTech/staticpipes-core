import collections
import os.path

import jinja2
import jinja2.meta

import staticpipes.utils
from staticpipes.current_info import CurrentInfo
from staticpipes.pipe_base import BasePipe


class PipeJinja2(BasePipe):
    """A pipeline that builds Jinja2 templates to output files

    Pass:

    - extensions - a list of file extensions that will be copied
    eg ["jinja2"].
    defaults to ["html"]

    """

    def __init__(self, extensions=["html"]):
        self.extensions = extensions
        self.jinja2_env = None
        self._templates_that_have_unknown_dependents: list = []
        self._templates_dependents: dict = collections.defaultdict(list)

    def start_build(self, current_info: CurrentInfo) -> None:
        self.jinja2_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.source_directory.dir),
            autoescape=jinja2.select_autoescape(),
        )

    def _actually_build_template(
        self, dir: str, filename: str, current_info: CurrentInfo
    ) -> None:
        # print("JINJA2 {} {}".format(dir, filename))
        template = self.jinja2_env.get_template(os.path.join(dir, filename))
        contents = template.render(current_info.context)
        self.build_directory.write(dir, filename, contents)

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        self._actually_build_template(dir, filename, current_info)

        if current_info.watch:
            ast = self.jinja2_env.parse(
                source=self.source_directory.get_contents_as_str(dir, filename),
                filename=os.path.join(dir, filename),
            )

            for t in jinja2.meta.find_referenced_templates(ast):
                if t:
                    if not t.startswith("/"):
                        t = "/" + t
                    self._templates_dependents[t].append((dir, filename))
                else:
                    self._templates_that_have_unknown_dependents.append((dir, filename))

    def file_changed_during_watch(self, dir, filename, current_info):
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        # Build ourself
        self._actually_build_template(dir, filename, current_info)

        # Look for any dependent templates for this one
        for x in self._templates_dependents.get(
            staticpipes.utils.make_path_from_dir_and_filename(dir, filename), []
        ):
            self._actually_build_template(x[0], x[1], current_info)

        # If a template has unknown dependents, build it anyway,
        # as it *might* depend on this one.
        for x in self._templates_that_have_unknown_dependents:
            if x[0] != dir or x[1] != filename:
                self._actually_build_template(x[0], x[1], current_info)

    def file_changed_but_excluded_during_watch(self, dir, filename, current_info):
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        # If it has the right extension, we still look for other templates to build

        # Look for any dependent templates for this one
        for x in self._templates_dependents.get(
            staticpipes.utils.make_path_from_dir_and_filename(dir, filename), []
        ):
            self._actually_build_template(x[0], x[1], current_info)

        # If a template has unknown dependents, build it anyway,
        # as it *might* depend on this one.
        for x in self._templates_that_have_unknown_dependents:
            self._actually_build_template(x[0], x[1], current_info)
