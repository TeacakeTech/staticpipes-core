import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.javascript_minifier
import staticpipes.watcher
import staticpipes.worker


def test_javascript_minifier():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.javascript_minifier.PipeJavascriptMinifier()],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "javascript_with_comments",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "main.js"))
    with open(os.path.join(out_dir, "main.js")) as fp:
        contents = fp.read()
    assert """var x="cat";""" == contents
