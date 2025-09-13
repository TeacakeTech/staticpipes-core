from typing import Optional

from staticpipes.jinja2_environment import Jinja2Environment
from staticpipes.process_base import BaseProcessor


class ProcessJinja2RenderContents(BaseProcessor):
    """
    Renders the current contents as a Jinja2 template.
    """

    def __init__(self, jinja2_environment: Optional[Jinja2Environment] = None):
        self._jinja2_environment: Optional[Jinja2Environment] = jinja2_environment

    def process_file(
        self, source_dir, source_filename, process_current_info, current_info
    ):
        """"""

        if not self._jinja2_environment:
            self._jinja2_environment = Jinja2Environment()
        template = self._jinja2_environment.get(
            source_directory=self.source_directory
        ).from_string(process_current_info.contents)
        contents = template.render(process_current_info.context)
        process_current_info.contents = contents
