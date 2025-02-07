import os
import shutil
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.jinja2
import staticpipes.worker


def test_jinja2():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.jinja2.PipeJinja2(extensions=["html"])],
        context={"hello": "World"},
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
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()

    contents = "".join([i.strip() for i in contents.split("\n")])

    assert (
        "<!doctype html><html><head></head><body>Hello World</body></html>" == contents
    )


def test_jinja2_then_watch(monkeypatch):
    monkeypatch.setattr(staticpipes.watcher.Watcher, "watch", lambda self: None)
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "jinja2_and_exclude_underscore_directories",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[staticpipes.pipes.jinja2.PipeJinja2(extensions=["html"])],
        context={"hello": "World"},
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(in_dir, "in"),
        out_dir,
    )
    # run
    worker.watch()
    # test 1
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head></head><body>Hello World</body></html>" == contents
    )
    # Edit index.html
    with open(os.path.join(in_dir, "in", "index.html")) as fp:
        contents = fp.read()
    with open(os.path.join(in_dir, "in", "index.html"), "w") as fp:
        fp.write(contents.replace("Hello", "Goodbye"))
    # Manually trigger watch handler
    worker.process_file_during_watch("/", "index.html")
    # test 2
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head></head><body>Goodbye World</body></html>"
        == contents
    )
