import os

import staticpipes.build_directory
import staticpipes.checks.html_tags
import staticpipes.config
import staticpipes.pipes.collection_records_process
import staticpipes.pipes.load_collection_csv
import staticpipes.processes.jinja2
import staticpipes.watcher
import staticpipes.worker


def test_check_html_tags():
    # setup
    config = staticpipes.config.Config(
        checks=[staticpipes.checks.html_tags.CheckHtmlTags()]
    )
    build_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fixtures",
        "html_tags",
    )
    worker = staticpipes.worker.Worker(
        config,
        build_dir,
        build_dir,
    )
    # run
    worker._check()
    # test
    check_reports = worker._check_reports
    assert [i.json() for i in check_reports] == [
        {
            "type": "html_tag_missing_attribute",
            "dir": "/",
            "file": "index.html",
            "message": "Tag img is missing attribute alt",
            "line": 3,
            "column": 8,
            "generator": {
                "class": "CheckHtmlTags",
            },
        },
        {
            "type": "html_tag_missing_attribute",
            "dir": "/",
            "file": "index.html",
            "message": "Tag img is missing attribute alt",
            "line": 4,
            "column": 8,
            "generator": {
                "class": "CheckHtmlTags",
            },
        },
    ]
