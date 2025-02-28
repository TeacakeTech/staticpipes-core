import os
import shutil
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipes.copy_with_versioning
import staticpipes.pipes.jinja2
import staticpipes.worker


def test_copy_fixture():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.copy_with_versioning.PipeCopyWithVersioning(
                extensions=["css", "js"], context_key="where_my_files"
            ),
            staticpipes.pipes.jinja2.PipeJinja2(extensions=["html"]),
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "copy_with_versioning_then_jinja2",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test original file not there
    assert not os.path.exists(os.path.join(out_dir, "styles.main.css"))
    assert not os.path.exists(os.path.join(out_dir, "js", "main.js"))
    # test file with hash there
    assert os.path.exists(
        os.path.join(out_dir, "styles.main.73229b70fe5f1ad4bf6e6ef249287ad4.css")
    )
    assert os.path.exists(
        os.path.join(out_dir, "js", "main.ceba641cf86025b52dfc12a1b847b4d8.js")
    )
    # test details in context for later pipes to use
    assert {
        "where_my_files": {
            "/styles.main.css": "/styles.main.73229b70fe5f1ad4bf6e6ef249287ad4.css",
            "/js/main.js": "/js/main.ceba641cf86025b52dfc12a1b847b4d8.js",
        }
    } == worker.current_info.get_context()
    # test HTML
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        """<!doctype html><html><head><link href="/styles.main.73229b70fe5f1ad4bf6e6ef249287ad4.css" rel="stylesheet"/></head><body><script src="/js/main.ceba641cf86025b52dfc12a1b847b4d8.js"></script></body></html>"""  # noqa
        == contents
    )


def test_watch_while_change_js_file(monkeypatch):
    monkeypatch.setattr(staticpipes.watcher.Watcher, "watch", lambda self: None)
    # setup
    in_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    shutil.copytree(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "copy_with_versioning_then_jinja2",
        ),
        os.path.join(in_dir, "in"),
    )
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.pipes.copy_with_versioning.PipeCopyWithVersioning(
                extensions=["css", "js"], context_key="where_my_files"
            ),
            staticpipes.pipes.jinja2.PipeJinja2(extensions=["html"]),
        ],
        context={},
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
    assert "/js/main.ceba641cf86025b52dfc12a1b847b4d8.js" in contents
    # Edit JS File
    with open(os.path.join(in_dir, "in", "js", "main.js")) as fp:
        contents = fp.read()
    with open(os.path.join(in_dir, "in", "js", "main.js"), "w") as fp:
        fp.write(contents.replace("hello", "goodbye"))
    # Manually trigger watch handler
    worker.process_file_during_watch("js", "main.js")
    # test 2 - js filename has changed,
    # because we picked up the context changed
    # and called  context_changed_during_watch on PipeJinja2
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    assert "/js/main.e925391dce77e33cd5a0d760f9c0b6d1.js" in contents
