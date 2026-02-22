import logging
import os

from markdown_it import MarkdownIt

from staticpipes.bundles.python_docs import BundlePythonDocs
from staticpipes.checks.html_tags import CheckHtmlTags
from staticpipes.checks.html_with_tidy import CheckHtmlWithTidy
from staticpipes.checks.internal_links import CheckInternalLinks
from staticpipes.config import Config
from staticpipes.jinja2_environment import Jinja2Environment
from staticpipes.pipes.copy import PipeCopy
from staticpipes.pipes.exclude_underscore_directories import (
    PipeExcludeUnderscoreDirectories,
)
from staticpipes.pipes.process import PipeProcess
from staticpipes.process_base import BaseProcessor
from staticpipes.processes.change_extension import ProcessChangeExtension
from staticpipes.processes.jinja2 import ProcessJinja2
from staticpipes.processes.markdown_yaml_to_html_context import (
    ProcessMarkdownYAMLToHTMLContext,
)


def render_markdown(content):
    md = MarkdownIt()
    return md.render(content) if content else ""


jinja2_environment = Jinja2Environment(filters={"render_markdown": render_markdown})


class ProcessMarkdownPages(BaseProcessor):

    def process_source_file(
        self,
        source_dir: str,
        source_filename: str,
        process_current_info,
        current_info,
    ):
        # Change all files to be in a directory with index.html
        # so we don't get .html in our site
        filename_main_bit = process_current_info.filename[:-5]
        if filename_main_bit != "index":
            process_current_info.filename = "index.html"
            process_current_info.dir = (
                filename_main_bit
                if process_current_info.dir == "/"
                else process_current_info.dir + "/" + filename_main_bit
            )
        # Add extra info we'll use in template
        breadcrumbs = []
        path = ""
        source_dir_bits = [i for i in source_dir.split("/") if i]
        for dir in source_dir_bits:
            path += dir + "/"
            breadcrumbs.append((path, dir))

        if source_filename != "index.md":
            breadcrumbs.append((None, process_current_info.context.get("title")))

        process_current_info.context["breadcrumbs"] = breadcrumbs


version = os.getenv("VERSION", "")

config = Config(
    [
        PipeExcludeUnderscoreDirectories(),
        PipeProcess(
            extensions=["md"],
            processors=[
                ProcessMarkdownYAMLToHTMLContext(),
                ProcessChangeExtension("html"),
                ProcessMarkdownPages(),
                ProcessJinja2(
                    template="_templates/content.html",
                    jinja2_environment=jinja2_environment,
                ),
            ],
        ),
        BundlePythonDocs(
            module_names=["staticpipes"], jinja2_environment=jinja2_environment
        ),
        PipeCopy(extensions=["css"]),
    ],
    checks=[
        CheckHtmlWithTidy(),
        CheckHtmlTags(),
        CheckInternalLinks(),
    ],
    context={
        "base_url": "/{}/".format(version) if version else "/",
        "version": version if version else "dev",
        "meta_robots": "index, follow" if version == "stable" else "noindex, nofollow",
    },
)


if __name__ == "__main__":
    from staticpipes.cli import cli

    cli(
        config,
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs"),
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "_site"),
        log_level=logging.DEBUG,
    )
