import os
import pathlib
import shutil
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.copy
import staticpipes.watcher
import staticpipes.worker


def test_copy_fixture_with_extensions():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.copy.PipeCopy(extensions=["html"])],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures", "copy"),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert not os.path.exists(os.path.join(out_dir, "readme.md"))


def test_copy_fixture_with_no_extensions():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.copy.PipeCopy()],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures", "copy"),
        out_dir,
    )
    # run
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert os.path.exists(os.path.join(out_dir, "readme.md"))


def test_copy_fixture_then_watch(monkeypatch):
    monkeypatch.setattr(staticpipes.watcher.Watcher, "watch", lambda self: None)
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures", "copy"),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.copy.PipeCopy(extensions=["html"])],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # run
    worker.watch()
    # test 1
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert not os.path.exists(os.path.join(out_dir, "about.html"))
    assert not os.path.exists(os.path.join(out_dir, "readme.md"))
    # Create file
    with open(os.path.join(in_dir, "in", "about.html"), "w") as fp:
        fp.write("About")
    # Manually trigger watch handler
    worker.process_file_during_watch("/", "about.html")
    # test 2
    assert os.path.exists(os.path.join(out_dir, "about.html"))


def test_copy_ignore_dist_under_source():
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "copy",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = os.path.join(in_dir, "in", "_site")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.copy.PipeCopy(extensions=["html"])],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # run twice
    # The second time it should ignore the site folder under the src folder
    print("Build 1")
    worker.build()
    print("Build 2")
    worker.build()
    # test
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    assert not os.path.exists(os.path.join(out_dir, "_site", "index.html"))


def test_copy_and_delete_files_already_in_site_dir():
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "copy",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.copy.PipeCopy(extensions=["html"])],
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
