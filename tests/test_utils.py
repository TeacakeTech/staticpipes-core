import pytest

import staticpipes.utils


@pytest.mark.parametrize(
    "dir, filename, out",
    [
        ("/", "index.html", "/index.html"),
        ("", "index.html", "/index.html"),
        ("assets", "main.css", "/assets/main.css"),
        ("/assets", "main.css", "/assets/main.css"),
    ],
)
def test_make_path_from_dir_and_filename(dir, filename, out):
    assert staticpipes.utils.make_path_from_dir_and_filename(dir, filename) == out


@pytest.mark.parametrize(
    "path, dir, filename",
    [
        ("/index.html", "", "index.html"),
        ("/blog/index.html", "/blog", "index.html"),
        ("/blog/2025/index.html", "/blog/2025", "index.html"),
        ("blog/index.html", "/blog", "index.html"),
    ],
)
def test_make_dir_and_filename_from_path(path, dir, filename):
    o1, o2 = staticpipes.utils.make_dir_and_filename_from_path(path)
    assert o1 == dir
    assert o2 == filename
