import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipelines.copy
import staticpipes.worker
from staticpipes.pipelines.exclude_underscore_directories import (
    PipeLineExcludeUnderscoreDirectories,
)


def test_exclude_underscore_directories():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipelines=[
            PipeLineExcludeUnderscoreDirectories(),
            staticpipes.pipelines.copy.PipeLineCopy(),
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "jinja2_and_exclude_underscore_directories",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert not os.path.exists(os.path.join(out_dir, "_templates", "base.html"))
