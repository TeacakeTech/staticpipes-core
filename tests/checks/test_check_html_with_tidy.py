import os

import staticpipes.build_directory
import staticpipes.checks.html_with_tidy
import staticpipes.config
import staticpipes.pipes.collection_records_process
import staticpipes.pipes.load_collection_csv
import staticpipes.processes.jinja2
import staticpipes.watcher
import staticpipes.worker


def test_check_html_with_tidy():
    # setup
    config = staticpipes.config.Config(
        checks=[staticpipes.checks.html_with_tidy.CheckHtmlWithTidy()]
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
            "type": "html_with_tidy",
            "dir": "/",
            "file": "index.html",
            "message": "line 1 column 1 - Warning: missing <!DOCTYPE> declaration",
            "line": 1,
            "column": 1,
            "generator": {
                "class": "CheckHtmlWithTidy",
            },
        },
        {
            "type": "html_with_tidy",
            "dir": "/",
            "file": "index.html",
            "message": "line 2 column 5 - Warning: inserting missing 'title' element",
            "line": 2,
            "column": 5,
            "generator": {
                "class": "CheckHtmlWithTidy",
            },
        },
        {
            "type": "html_with_tidy",
            "dir": "/",
            "file": "index.html",
            "message": 'line 3 column 9 - Warning: <img> lacks "alt" attribute',
            "line": 3,
            "column": 9,
            "generator": {
                "class": "CheckHtmlWithTidy",
            },
        },
    ]
