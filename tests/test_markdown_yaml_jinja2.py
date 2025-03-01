import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.process
import staticpipes.processes.change_extension
import staticpipes.processes.jinja2
import staticpipes.processes.markdown_yaml_to_html_context
import staticpipes.watcher
import staticpipes.worker


def test_markdown_yaml_jinja2():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.process.PipeProcess(
                extensions=["md"],
                processors=[
                    staticpipes.processes.markdown_yaml_to_html_context.ProcessMarkdownYAMLToHTMLContext(),  # noqa
                    staticpipes.processes.jinja2.ProcessJinja2("base.html"),
                    staticpipes.processes.change_extension.ProcessChangeExtension(
                        "html"
                    ),
                ],
            )
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "markdown_yaml_jinja2",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    assert (
        """<!doctype html><html><head><title>Hello World</title></head><body><h1>Hello World</h1></body></html>"""  # noqa
        == "".join([i.strip() for i in contents.split("\n")])
    )
