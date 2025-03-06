import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.watcher
import staticpipes.worker
from staticpipes.pipes.python_document_process import PipePythonDocumentProcess
from staticpipes.processes.jinja2 import ProcessJinja2


def test_copy_fixture_with_extensions():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            PipePythonDocumentProcess(
                pkgutil_walk_packages_args=[
                    (
                        [
                            os.path.join(
                                os.path.dirname(os.path.realpath(__file__)),
                                "..",
                                "staticpipes",
                            )
                        ],
                        "staticpipes.",
                    )
                ],
                module_names=["staticpipes"],
                output_dir="",
                processors=[
                    ProcessJinja2(template="template.html"),
                ],
            ),
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "python_document_process",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test staticpipes
    assert os.path.exists(os.path.join(out_dir, "staticpipes.html"))
    with open(os.path.join(out_dir, "staticpipes.html")) as fp:
        contents = fp.read()
    assert "<h1>staticpipes</h1>" in contents

    # test staticpipes.worker
    assert os.path.exists(os.path.join(out_dir, "staticpipes.worker.html"))
    with open(os.path.join(out_dir, "staticpipes.worker.html")) as fp:
        contents = fp.read()
    assert "<h1>staticpipes.worker</h1>" in contents
