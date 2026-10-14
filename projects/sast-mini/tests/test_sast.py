import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from sast import scan_source  # noqa: E402


@settings(max_examples=200, deadline=None)
@given(st.text(max_size=300))
def test_scanner_never_crashes_on_arbitrary_input(src):
    assert isinstance(scan_source(src), list)


@settings(max_examples=100, deadline=None)
@given(st.from_regex(r"[a-z_][a-z0-9_]{0,10}", fullmatch=True))
def test_findings_are_sorted_by_line(name):
    src = f"import os\n{name} = 1\nos.system('ls')\neval('1')\n"
    lines = [f.line for f in scan_source(src)]
    assert lines == sorted(lines)