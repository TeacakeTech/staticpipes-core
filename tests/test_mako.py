import os
import shutil
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.exclude_underscore_directories
import staticpipes.pipes.jinja2
import staticpipes.pipes.mako
import staticpipes.watcher
import staticpipes.worker


def test_mako_then_watch_while_change_output_file(monkeypatch):
    monkeypatch.setattr(staticpipes.watcher.Watcher, "watch", lambda self: None)
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "mako_and_exclude_underscore_directories",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    mako_pipeline = staticpipes.pipes.mako.PipeMako(extensions=["html"])
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.exclude_underscore_directories.PipeExcludeUnderscoreDirectories(),  # noqa
            mako_pipeline,
        ],
        context={"hello": "World"},
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # run
    worker.watch()
    # test no _templates
    assert not os.path.exists(os.path.join(out_dir, "_templates", "base.html"))
    # test 1
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Hello</title></head><body>Hello World</body></html>"  # noqa
        == contents
    )
    # Edit index.html
    with open(os.path.join(in_dir, "in", "index.html")) as fp:
        contents = fp.read()
    with open(os.path.join(in_dir, "in", "index.html"), "w") as fp:
        fp.write(contents.replace("Hello", "Goodbye"))
    # Manually trigger watch handler, and test which templates are actually built
    worker.process_file_during_watch("/", "index.html")
    # test 2
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Hello</title></head><body>Goodbye World</body></html>"  # noqa
        == contents
    )


def test_mako_then_watch_while_change_base_template(monkeypatch):
    monkeypatch.setattr(staticpipes.watcher.Watcher, "watch", lambda self: None)
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "mako_and_exclude_underscore_directories",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    mako_pipeline = staticpipes.pipes.mako.PipeMako(extensions=["html"])
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.exclude_underscore_directories.PipeExcludeUnderscoreDirectories(),  # noqa
            mako_pipeline,
        ],
        context={"hello": "World"},
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # run
    worker.watch()
    # test no _templates
    assert not os.path.exists(os.path.join(out_dir, "_templates", "base.html"))
    # test 1
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Hello</title></head><body>Hello World</body></html>"  # noqa
        == contents
    )
    # Edit index.html
    with open(os.path.join(in_dir, "in", "_templates", "base.html")) as fp:
        contents = fp.read()
    with open(os.path.join(in_dir, "in", "_templates", "base.html"), "w") as fp:
        fp.write(contents.replace("Hello", "Goodbye"))
    # Manually trigger watch handler, and test which templates are actually built
    worker.process_file_during_watch("/", "base.html")
    # test 2
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Goodbye</title></head><body>Hello World</body></html>"  # noqa
        == contents
    )
