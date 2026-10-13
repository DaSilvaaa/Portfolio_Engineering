import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from analyzer import LogAnalyzer


def test_detect_sqli():
    analyzer = LogAnalyzer()
    alert = analyzer.analyze_web_log_entry("192.168.1.50", "/api/products?id=1' OR '1'='1", 200)
    assert alert is not None
    assert alert.rule == "SQL_INJECTION"
    assert alert.severity == "HIGH"


def test_detect_path_traversal():
    analyzer = LogAnalyzer()
    alert = analyzer.analyze_web_log_entry("10.0.0.12", "/files?download=../../etc/passwd", 403)
    assert alert is not None
    assert alert.rule == "PATH_TRAVERSAL"
    assert alert.severity == "HIGH"


def test_brute_force_threshold():
    analyzer = LogAnalyzer(brute_force_threshold=3)
    attacker_ip = "203.0.113.195"

    assert analyzer.analyze_auth_attempt(attacker_ip, success=False) is None
    assert analyzer.analyze_auth_attempt(attacker_ip, success=False) is None

    alert = analyzer.analyze_auth_attempt(attacker_ip, success=False)
    assert alert is not None
    assert alert.rule == "BRUTE_FORCE_DETECTED"
    assert alert.severity == "CRITICAL"


def test_successful_auth_resets_counter():
    analyzer = LogAnalyzer(brute_force_threshold=3)
    ip = "192.168.1.10"

    analyzer.analyze_auth_attempt(ip, success=False)
    analyzer.analyze_auth_attempt(ip, success=False)
    assert analyzer.analyze_auth_attempt(ip, success=True) is None
    assert analyzer.analyze_auth_attempt(ip, success=False) is None