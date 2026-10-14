import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from audit import entropy_bits  # noqa: E402


@settings(max_examples=200, deadline=None)
@given(st.text(max_size=64))
def test_entropy_is_never_negative(pw):
    assert entropy_bits(pw) >= 0.0


@settings(max_examples=200, deadline=None)
@given(st.text(min_size=1, max_size=64), st.sampled_from(list("aZ9!")))
def test_appending_a_character_never_lowers_entropy(pw, ch):
    assert entropy_bits(pw + ch) >= entropy_bits(pw)