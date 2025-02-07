import os.path

import jinja2

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

    def build_file(self, dir: str, filename: str, current_info: CurrentInfo) -> None:
        if not staticpipes.utils.does_filename_have_extension(
            filename, self.extensions
        ):
            return

        if not self.jinja2_env:
            self.jinja2_env = jinja2.Environment(
                loader=jinja2.FileSystemLoader(self.source_directory.dir),
                autoescape=jinja2.select_autoescape(),
            )

        # print("JINJA2 {} {}".format(dir, filename))
        template = self.jinja2_env.get_template(os.path.join(dir, filename))
        contents = template.render(current_info.context)
        self.build_directory.write(dir, filename, contents)

    def file_changed_during_watch(self, dir, filename, current_info):
        self.build_file(dir, filename, current_info)
