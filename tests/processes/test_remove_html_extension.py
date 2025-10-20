import pytest

import staticpipes.current_info
import staticpipes.process_current_info
import staticpipes.processes.remove_html_extension


@pytest.mark.parametrize(
    "dir_in, file_in, dir_out, file_out",
    [
        ("", "index.html", "", "index.html"),
        ("cats", "index.html", "cats", "index.html"),
        ("", "cats.html", "/cats", "index.html"),
        ("pets", "cats.html", "pets/cats", "index.html"),
    ],
)
def test_remove_html_extension(dir_in, file_in, dir_out, file_out):
    p = staticpipes.processes.remove_html_extension.ProcessRemoveHTMLExtension()
    ci = staticpipes.current_info.CurrentInfo()
    pci = staticpipes.process_current_info.ProcessCurrentInfo(dir_in, file_in, "", {})
    p.process_file(dir_in, file_in, pci, ci)
    assert dir_out == pci.dir
    assert file_out == pci.filename
