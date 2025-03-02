import os
import tempfile

import staticpipes.build_directory
import staticpipes.config
import staticpipes.datatig.pipes.load_datatig
import staticpipes.pipes.collection_items_jinja2
import staticpipes.pipes.javascript_minifier
import staticpipes.watcher
import staticpipes.worker


def test_items_jinja2():
    # setup
    out_dir = tempfile.mkdtemp(prefix="staticpipes_tests_")
    config = staticpipes.config.Config(
        pipes=[
            staticpipes.datatig.pipes.load_datatig.LoadDatatig(),
            staticpipes.pipes.collection_items_jinja2.CollectionItemsJinja2(
                type_id="datas", jinja2_template="_templates/item.html"
            ),  # noqa
        ],
    )
    worker = staticpipes.worker.Worker(
        config,
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "fixtures",
            "site_1",
        ),
        out_dir,
    )
    # run
    worker.build()
    # test
    with open(os.path.join(out_dir, "datas", "1.html")) as fp:
        contents = fp.read()
    contents = "".join([i.strip() for i in contents.split("\n")])
    assert (
        "<!doctype html><html><head><title>Hello</title></head><body><h1>One</h1></body></html>"  # noqa
        == contents
    )
