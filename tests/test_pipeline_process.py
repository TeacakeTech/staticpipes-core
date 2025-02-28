import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.process
import staticpipes.processes.javascript_minifier
import staticpipes.processes.version
import staticpipes.watcher
import staticpipes.worker


def test_copy_fixture_with_extensions():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.process.PipeProcess(
                extensions=["js"],
                processors=[
                    staticpipes.processes.javascript_minifier.ProcessJavascriptMinifier(),  # noqa
                    staticpipes.processes.version.ProcessVersion(),
                ],
            )
        ],
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
    assert os.path.exists(
        os.path.join(out_dir, "main.b1cee5ed8ca8405563a5be2227ddab36.js")
    )
    assert not os.path.exists(os.path.join(out_dir, "main.js"))

    with open(os.path.join(out_dir, "main.b1cee5ed8ca8405563a5be2227ddab36.js")) as fp:
        contents = fp.read()
    assert """var x="cat";""" == contents

    assert {
        "versioning_new_filenames": {
            "/main.js": "/main.b1cee5ed8ca8405563a5be2227ddab36.js",
        }
    } == worker.current_info.get_context()
