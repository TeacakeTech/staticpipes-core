import pytest

from staticpipes.source_directory import SourceDirectory


@pytest.mark.parametrize(
    "start_dir, dir, filename, expected",
    [
        ("/site", "/", "index.html", "/site/index.html"),
        ("/site", "cats", "index.html", "/site/cats/index.html"),
        ("/site", "/cats/", "index.html", "/site/cats/index.html"),
    ],
)
def test_get_full_filename(start_dir, dir, filename, expected):
    source_dir = SourceDirectory(start_dir)
    assert expected == source_dir.get_full_filename(dir, filename)
