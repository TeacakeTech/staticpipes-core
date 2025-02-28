import pytest

import staticpipes.current_info


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
def test_current_info_context(start, key, value, out):
    ci = staticpipes.current_info.CurrentInfo(start)
    ci.set_context(key, value)
    assert out == ci.get_context()
