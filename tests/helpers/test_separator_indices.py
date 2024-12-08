from msfabricutils.helpers import _separator_indices


def test_seperator_indices_simple_string():
    chars = "text.to.be.tested"
    assert _separator_indices(chars, ".") == [4, 7, 10]


def test_seperator_indices_string_with_quotes():
    chars = "'te.xt'.to.be.tested"
    assert _separator_indices(chars, ".") == [7, 10, 13]


def test_seperator_indices_string_with_both_quotes():
    chars = """'te"."xt'.to.be.tested"""
    assert _separator_indices(chars, ".") == [9, 12, 15]


def test_seperator_indices_only_dots():
    chars = "..."
    assert _separator_indices(chars, ".") == [0, 1, 2]


def test_seperator_indices_start_and_end_with_dots():
    chars = ".my-text."
    assert _separator_indices(chars, ".") == [0, 8]
