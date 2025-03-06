import logging
import os

from staticpipes.config import Config
from staticpipes.pipes.exclude_underscore_directories import (
    PipeExcludeUnderscoreDirectories,
)
from staticpipes.pipes.process import PipeProcess
from staticpipes.pipes.pydoc import PipePydoc
from staticpipes.processes.change_extension import ProcessChangeExtension
from staticpipes.processes.jinja2 import ProcessJinja2
from staticpipes.processes.markdown_yaml_to_html_context import (
    ProcessMarkdownYAMLToHTMLContext,
)

config = Config(
    pipes=[
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(
            extensions=["md"],
            processors=[
                ProcessMarkdownYAMLToHTMLContext(),
                ProcessJinja2(template="_templates/base.html"),
                ProcessChangeExtension("html"),
            ],
        ),
        PipePydoc(
            pydoc_dir=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "staticpipes"
            ),
            pydoc_pkgpath="staticpipes.",
            output_dir="reference",
            processors=[
                ProcessJinja2(template="_templates/base.html"),
            ],
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
