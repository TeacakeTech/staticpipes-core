import os
import tempfile

import pytest

import staticpipes.build_directory
import staticpipes.config
import staticpipes.jinja2_environment
import staticpipes.pipes.exclude_underscore_directories
import staticpipes.pipes.jinja2
import staticpipes.pipes.process
import staticpipes.processes.jinja2_render_contents
import staticpipes.watcher
import staticpipes.worker


@pytest.mark.parametrize(
    "jinja2_environment,expected_hello_var_output_in_html",
    [
        (None, "World &lt;3"),
        (staticpipes.jinja2_environment.Jinja2Environment(), "World &lt;3"),
        (
            staticpipes.jinja2_environment.Jinja2Environment(autoescape=False),
            "World <3",
        ),
    ],
)
def test_jinja2_render_contents(jinja2_environment, expected_hello_var_output_in_html):
    # setup
    in_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "fixtures",
        "jinja2_and_exclude_underscore_directories",
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes_and_groups_of_pipes=[
            staticpipes.pipes.exclude_underscore_directories.PipeExcludeUnderscoreDirectories(),  # noqa
            staticpipes.pipes.process.PipeProcess(
                extensions=["html"],
                processors=[
                    staticpipes.processes.jinja2_render_contents.ProcessJinja2RenderContents(  # noqa
                        jinja2_environment=jinja2_environment
                    ),  # noqa
                ],
            ),
        ],
        context={"hello": "World <3"},
    )
    worker = staticpipes.worker.Worker(
        config,
        in_dir,
        out_dir,
    )
    # run
    worker.build()
    # test
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Hello</title></head><body><h1>Hello</h1>Hello "  # noqa
        + expected_hello_var_output_in_html
        + "</body></html>"
        == contents
    )
