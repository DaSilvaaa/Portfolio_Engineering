import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


@dataclass
class SecurityAlert:
    severity: str
    ip: str
    rule: str
    description: str


class LogAnalyzer:
    SQLI_PATTERN = re.compile(
        r"(union\s+select|select\s+.*\s+from|'\s*or\s*'1'\s*=\s*'1|--|#)",
        re.IGNORECASE,
    )
    PATH_TRAVERSAL_PATTERN = re.compile(r"(\.\./|\.\.\\|/etc/passwd|/windows/win\.ini)")

    def __init__(self, brute_force_threshold: int = 5):
        self.brute_force_threshold = brute_force_threshold
        self.failed_attempts = defaultdict(int)

    def analyze_web_log_entry(self, ip: str, path: str, status_code: int) -> Optional[SecurityAlert]:
        if self.SQLI_PATTERN.search(path):
            return SecurityAlert(
                severity="HIGH",
                ip=ip,
                rule="SQL_INJECTION",
                description=f"Tentativa de injeção SQL detetada no path: {path}",
            )

        if self.PATH_TRAVERSAL_PATTERN.search(path):
            return SecurityAlert(
                severity="HIGH",
                ip=ip,
                rule="PATH_TRAVERSAL",
                description=f"Tentativa de Directory Traversal no path: {path}",
            )

        return None

    def analyze_auth_attempt(self, ip: str, success: bool) -> Optional[SecurityAlert]:
        if success:
            self.failed_attempts[ip] = 0
            return None

        self.failed_attempts[ip] += 1
        if self.failed_attempts[ip] >= self.brute_force_threshold:
            return SecurityAlert(
                severity="CRITICAL",
                ip=ip,
                rule="BRUTE_FORCE_DETECTED",
                description=f"IP excedeu o limite com {self.failed_attempts[ip]} tentativas falhadas consecutivas.",
            )
        return None