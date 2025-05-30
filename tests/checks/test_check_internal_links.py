import os

import pytest

import staticpipes.build_directory
import staticpipes.checks.internal_links
import staticpipes.config
import staticpipes.pipes.collection_records_process
import staticpipes.pipes.load_collection_csv
import staticpipes.processes.jinja2
import staticpipes.watcher
import staticpipes.worker


@pytest.mark.parametrize(
    "html, links",
    [
        ('<a href="cats.html">Cats</a>', ["cats.html"]),
        ('<img src="cats.png">', ["cats.png"]),
        ('<link rel="stylesheet" href="style.css">', ["style.css"]),
        ('<script src="script.js">', ["script.js"]),
    ],
)
def test_check_internal_links_html_parser(html, links):

    parser = staticpipes.checks.internal_links.CheckInternalLinksHTMLParser(
        lambda x: True
    )
    parser.feed(html)
    assert links == [i["link"] for i in parser.links]


@pytest.mark.parametrize(
    "source_dir, souce_filename, link, expected",
    [
        # Test absolute links
        (
            "/",
            "index.html",
            "/logo.png",
            [("", "logo.png"), ("/logo.png", "index.html")],
        ),
        (
            "/blog",
            "index.html",
            "/logo.png",
            [("", "logo.png"), ("/logo.png", "index.html")],
        ),
        # Test relative links ....
        # To same directory
        ("", "index.html", "logo.png", [("", "logo.png"), ("logo.png", "index.html")]),
        (
            "blog",
            "index.html",
            "logo.png",
            [("blog", "logo.png"), ("blog/logo.png", "index.html")],
        ),
        # Test a child dir of the starting point
        (
            "blog",
            "index.html",
            "images/logo.png",
            [("blog/images", "logo.png"), ("blog/images/logo.png", "index.html")],
        ),
        (
            "blog",
            "index.html",
            "images/full/logo.png",
            [
                ("blog/images/full", "logo.png"),
                ("blog/images/full/logo.png", "index.html"),
            ],
        ),
        # Test going up to a parent from the starting point
        (
            "blog",
            "index.html",
            "../logo.png",
            [("", "logo.png"), ("logo.png", "index.html")],
        ),
        # Go one higher than we can and make sure we don't crash
        (
            "blog",
            "index.html",
            "../../logo.png",
            [("", "logo.png"), ("logo.png", "index.html")],
        ),
    ],
)
def test_get_dirs_files_to_check(source_dir, souce_filename, link, expected):
    actual = staticpipes.checks.internal_links._get_dirs_files_to_check(
        source_dir, souce_filename, link
    )
    assert actual == expected


def test_check_internal_links():
    # setup
    config = staticpipes.config.Config(
        checks=[staticpipes.checks.internal_links.CheckInternalLinks()]
    )
    build_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "fixtures", "internal_links"
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
            "type": "missing_link",
            "dir": "/",
            "file": "index.html",
            "message": "Can not find internal link: /staticpopes.html",
            "line": 5,
            "column": 8,
            "generator": {
                "class": "CheckInternalLinks",
            },
        }
    ]
