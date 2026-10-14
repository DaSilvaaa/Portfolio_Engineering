import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sast import scan_source  # noqa: E402


def rules(src: str) -> list[str]:
    return [f.rule for f in scan_source(src)]


def test_eval_and_exec():
    assert rules("eval(x)\nexec(y)") == ["SAST001", "SAST001"]


def test_os_system_and_shell_true():
    assert rules("import os, subprocess\nos.system('ls')\nsubprocess.run('ls', shell=True)") == ["SAST002", "SAST003"]


def test_subprocess_without_shell_is_clean():
    assert rules("import subprocess\nsubprocess.run(['ls', '-l'])") == []


def test_pickle_and_weak_hash():
    assert rules("import pickle, hashlib\npickle.loads(b)\nhashlib.md5(b)") == ["SAST004", "SAST005"]


def test_yaml_load_requires_safe_loader():
    assert rules("import yaml\nyaml.load(s)") == ["SAST006"]
    assert rules("import yaml\nyaml.load(s, Loader=yaml.SafeLoader)") == []


def test_tls_verification_disabled():
    assert rules("import requests\nrequests.get(u, verify=False)") == ["SAST007"]


def test_hardcoded_secret_detected_but_env_is_clean():
    assert rules("password = 'hunter2hunter2'") == ["SAST008"]
    assert rules("import os\npassword = os.environ['PW']") == []
    assert rules("password = ''") == []


def test_syntax_error_reported_not_raised():
    assert rules("def (") == ["PARSE"]