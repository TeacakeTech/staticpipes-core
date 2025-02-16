import os
import tempfile

import pytest

from staticpipes.build_directory import BuildDirectory


@pytest.mark.parametrize(
    "dir, filename, walk_results",
    [
        ("/", "index.html", [("BASEDIR", [], ["index.html"])]),
        ("", "index.html", [("BASEDIR", [], ["index.html"])]),
        (
            "/blog",
            "index.html",
            [("BASEDIR", ["blog"], []), ("BASEDIR/blog", [], ["index.html"])],
        ),
        (
            "blog",
            "index.html",
            [("BASEDIR", ["blog"], []), ("BASEDIR/blog", [], ["index.html"])],
        ),
    ],
)
def test_write(dir, filename, walk_results):
    dir_path = tempfile.mkdtemp(prefix="staticpipes_tests_")
    build_directory = BuildDirectory(dir=dir_path)
    build_directory.write(dir, filename, "TEST")
    results = sorted(
        [(a.replace(dir_path, "BASEDIR"), b, c) for a, b, c in os.walk(dir_path)]
    )
    assert walk_results == results
