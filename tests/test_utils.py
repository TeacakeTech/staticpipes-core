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


@pytest.mark.parametrize(
    "check_dir, directories, result",
    [
        ("/", ["/"], True),
        ("/css", ["/"], True),
        ("/css", ["/css"], True),
        ("/css/prod", ["/css"], True),
        ("/", ["/css", "/js"], False),
        ("/js", ["/css"], False),
        ("/123", ["/1"], False),
        ("/1", ["/123"], False),
    ],
)
def test_is_directory_in_list(check_dir, directories, result):
    assert result == staticpipes.utils.is_directory_in_list(check_dir, directories)
