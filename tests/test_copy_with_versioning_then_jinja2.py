import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.pipelines.copy_with_versioning
import staticpipes.pipelines.jinja2
import staticpipes.worker


def test_copy_fixture():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipelines=[
            staticpipes.pipelines.copy_with_versioning.PipeLineCopyWithVersioning(
                extensions=["css", "js"], context_key="where_my_files"
            ),
            staticpipes.pipelines.jinja2.PipeLineJinja2(extensions=["html"]),
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
    # test details in context for later pipelines to use
    assert {
        "where_my_files": {
            "/styles.main.css": "/styles.main.73229b70fe5f1ad4bf6e6ef249287ad4.css",
            "/js/main.js": "/js/main.ceba641cf86025b52dfc12a1b847b4d8.js",
        }
    } == worker.current_info.context
    # test HTML
    assert os.path.exists(os.path.join(out_dir, "index.html"))
    with open(os.path.join(out_dir, "index.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        """<!doctype html><html><head><link href="/styles.main.73229b70fe5f1ad4bf6e6ef249287ad4.css" rel="stylesheet"/></head><body><script src="/js/main.ceba641cf86025b52dfc12a1b847b4d8.js"></script></body></html>"""  # noqa
        == contents
    )
