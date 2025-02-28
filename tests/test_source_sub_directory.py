import os
import tempfile

import pytest

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.copy
import staticpipes.pipes.copy_with_versioning
import staticpipes.watcher
import staticpipes.worker


@pytest.mark.parametrize(
    "source_sub_directory",
    [
        ("assets"),
        ("/assets"),
    ],
)
def test_source_sub_directory_copy(source_sub_directory):
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.copy.PipeCopy(
                extensions=["js", "txt"], source_sub_directory=source_sub_directory
            )
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "source_sub_directory",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "js", "main.js"))
    assert not os.path.exists(os.path.join(out_dir, "assets", "js", "main.js"))
    assert os.path.exists(os.path.join(out_dir, "robots.txt"))
    assert not os.path.exists(os.path.join(out_dir, "assets", "robots.txt"))


@pytest.mark.parametrize(
    "source_sub_directory",
    [
        ("assets"),
        ("/assets"),
    ],
)
def test_source_sub_directory_copy_with_versioning(source_sub_directory):
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.copy_with_versioning.PipeCopyWithVersioning(
                extensions=["js"], source_sub_directory=source_sub_directory
            )
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "source_sub_directory",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(
        os.path.join(out_dir, "js", "main.ceba641cf86025b52dfc12a1b847b4d8.js")
    )
    assert not os.path.exists(os.path.join(out_dir, "js", "main.js"))
    assert not os.path.exists(os.path.join(out_dir, "assets", "js", "main.js"))
    assert {
        "versioning_new_filenames": {
            "/js/main.js": "/js/main.ceba641cf86025b52dfc12a1b847b4d8.js",
        }
    } == worker.current_info.get_context()
