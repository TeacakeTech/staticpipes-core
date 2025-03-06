import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.watcher
import staticpipes.worker
from staticpipes.pipes.pydoc import PipePydoc
from staticpipes.processes.jinja2 import ProcessJinja2


def test_copy_fixture_with_extensions():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            PipePydoc(
                pydoc_dir=os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), "..", "staticpipes"
                ),
                pydoc_pkgpath="staticpipes.",
                output_dir="",
                processors=[
                    ProcessJinja2(template="template.html"),
                ],
            ),
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures", "pydoc"),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "staticpipes.worker.html"))
    with open(os.path.join(out_dir, "staticpipes.worker.html")) as fp:
        contents = fp.read()
    assert "process_file_during_watch" in contents
