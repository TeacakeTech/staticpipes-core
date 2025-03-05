import logging
import os

import staticpipes
from staticpipes.config import Config
from staticpipes.pipes.exclude_underscore_directories import (
    PipeExcludeUnderscoreDirectories,
)
from staticpipes.pipes.process import PipeProcess
from staticpipes.pipes.python_document import PipePythonDocument
from staticpipes.processes.change_extension import ProcessChangeExtension
from staticpipes.processes.jinja2 import ProcessJinja2
from staticpipes.processes.markdown_to_html import ProcessMarkdownToHTML
from staticpipes.processes.markdown_yaml_to_html_context import (
    ProcessMarkdownYAMLToHTMLContext,
)

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(
            processors=[
                ProcessMarkdownYAMLToHTMLContext(),
                ProcessMarkdownToHTML(),
                ProcessJinja2(template="_templates/base.html"),
                ProcessChangeExtension("html"),
            ]
        ),
        PipePythonDocument(
            packages=[staticpipes],
            output_dir="reference",
            jinja2_template="_templates/reference.html",
        ),
    ],
    context={},
)


if __name__ == "__main__":
    from staticpipes.cli import cli

    output_dir = (
        os.getenv("READTHEDOCS_OUTPUT") + "/html"
        if os.getenv("READTHEDOCS_OUTPUT")
        else "_site"
    )
    cli(
        config,
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs"),
        os.path.join(os.path.dirname(os.path.realpath(__file__)), output_dir),
        log_level=logging.DEBUG,
    )
