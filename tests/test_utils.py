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
def test_source_sub_directory_copy(dir, filename, out):
    assert staticpipes.utils.make_path_from_dir_and_filename(dir, filename) == out
