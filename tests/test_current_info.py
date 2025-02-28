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
    ci = staticpipes.current_info.CurrentInfo(start, watch=True)
    assert 0 == ci.get_context_version()
    ci.set_context(key, value)
    assert 1 == ci.get_context_version()
    assert out == ci.get_context()
