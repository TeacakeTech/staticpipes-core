import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.css_minifier
import staticpipes.pipes.process
import staticpipes.processes.css_minifier
import staticpipes.watcher
import staticpipes.worker


def test_css_minifier_pipe():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.css_minifier.PipeCSSMinifier()],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "css_with_comments",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "main.css"))
    with open(os.path.join(out_dir, "main.css")) as fp:
        contents = fp.read()
    assert """html{margin:0,padding:0}""" == contents


def test_css_minifier_process():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.process.PipeProcess(
                extensions=["css"],
                processors=[
                    staticpipes.processes.css_minifier.ProcessCSSMinifier(),  # noqa
                ],
            )
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "css_with_comments",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "main.css"))
    with open(os.path.join(out_dir, "main.css")) as fp:
        contents = fp.read()
    assert """html{margin:0,padding:0}""" == contents
