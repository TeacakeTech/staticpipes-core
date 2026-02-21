from typing import Optional

from staticpipes.jinja2_environment import Jinja2Environment
from staticpipes.process_base import BaseProcessor


class ProcessJinja2RenderSourceFile(BaseProcessor):
    """
    Renders a source file as a Jinja2 template.

    The current contents of the pipeline are put in the "content" variable
    in the context.

    Pass:

    - template - the path to the template in the source directory to render.

    """

    def __init__(
        self, template: str, jinja2_environment: Optional[Jinja2Environment] = None
    ):
        self._template = template
        self._jinja2_environment: Optional[Jinja2Environment] = jinja2_environment

    def process_source_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):
        """"""

        if not self._jinja2_environment:
            self._jinja2_environment = Jinja2Environment()

        template = self._jinja2_environment.get(
            source_directory=self._source_directory,
            secondary_source_directories=self._secondary_source_directories,
        ).get_template(self._template)
        process_current_info.context["content"] = process_current_info.contents
        contents = template.render(process_current_info.context)
        process_current_info.contents = contents
