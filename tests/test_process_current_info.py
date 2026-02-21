import pytest

import staticpipes.process_current_info


@pytest.mark.parametrize(
    "start, key, value, out",
    [
        ({}, "cat", True, {"cat": True}),
        ({}, ["cat", "floffy"], True, {"cat": {"floffy": True}}),
        (
            {"cat": {"tail": True}},
            ["cat", "floffy"],
            True,
            {"cat": {"floffy": True, "tail": True}},
        ),
    ],
)
def test_process_current_info_context(start, key, value, out):
    ci = staticpipes.process_current_info.ProcessCurrentInfo(
        "/", "index.html", "HOMEPAGE", start
    )
    ci.set_context(key, value)
    assert out == ci.context
