import os
import pathlib
import shutil
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.copy
import staticpipes.watcher
import staticpipes.worker


def test_copy_and_delete_files_already_in_site_dir():
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "fixtures",
            "copy",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes_and_groups_of_pipes=[
            staticpipes.pipes.copy.PipeCopy(extensions=["html"])
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # add extra file to out dir, then build
    pathlib.Path(os.path.join(out_dir, "old.html")).touch()
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert not os.path.exists(os.path.join(out_dir, "old.html"))


def test_copy_and_dont_delete_files_already_in_site_dir():
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "fixtures",
            "copy",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes_and_groups_of_pipes=[
            staticpipes.pipes.copy.PipeCopy(extensions=["html"])
        ],
        remove_build_directory_content_we_did_not_touch=False,
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # add extra file to out dir, then build
    pathlib.Path(os.path.join(out_dir, "old.html")).touch()
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert os.path.exists(os.path.join(out_dir, "old.html"))
