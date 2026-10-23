import sys
from pathlib import Path

import pytest
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

RULE_CASES = {
    "SAST001": "eval('1+1')",
    "SAST002": "import os\nos.system('ls')",
    "SAST003": "import subprocess\nsubprocess.run('ls', shell=True)",
    "SAST004": "import pickle\npickle.loads(b'')",
    "SAST005": "import hashlib\nhashlib.md5(b'x')",
    "SAST006": "import yaml\nyaml.load('a: 1')",
    "SAST007": "import requests\nrequests.get('https://x', verify=False)",
    "SAST008": "api_key = 'abcd1234'",
}


@pytest.mark.parametrize("rule,src", RULE_CASES.items())
def test_each_rule_detects_its_pattern(rule, src):
    assert rule in {f.rule for f in scan_source(src)}


@pytest.mark.parametrize(
    "src",
    [
        "import subprocess\nsubprocess.run(['ls'])",
        "import yaml\nyaml.safe_load('a: 1')",
        "import hashlib\nhashlib.sha256(b'x')",
        "import requests\nrequests.get('https://x')",
        "password = os.environ['PW']",
    ],
)
def test_safe_code_produces_no_findings(src):
    assert scan_source(src) == []


def test_syntax_error_reported_as_parse_finding():
    assert [f.rule for f in scan_source("def (:")] == ["PARSE"]
