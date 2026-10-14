import argparse
import ast
import json
import pathlib
import re
import sys
from dataclasses import asdict, dataclass

SEVERITY = {"low": 1, "medium": 2, "high": 3}
SECRET_NAME = re.compile(r"(passw(or)?d|secret|token|api_?key|private_?key)", re.I)
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "build", "dist"}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    file: str
    line: int
    message: str


def dotted(node: ast.AST) -> str:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def is_const(node: ast.AST | None, value) -> bool:
    return isinstance(node, ast.Constant) and node.value is value


class _Visitor(ast.NodeVisitor):
    def __init__(self, file: str):
        self.file = file
        self.findings: list[Finding] = []

    def add(self, node: ast.AST, rule: str, sev: str, msg: str):
        self.findings.append(Finding(rule, sev, self.file, getattr(node, "lineno", 0), msg))

    def visit_Call(self, node: ast.Call):
        name = dotted(node.func)
        kw = {k.arg: k.value for k in node.keywords if k.arg}
        if name in ("eval", "exec"):
            self.add(node, "SAST001", "high", f"uso de {name}() permite execução arbitrária de código")
        elif name == "os.system":
            self.add(node, "SAST002", "high", "os.system é vulnerável a injeção de comandos")
        elif name.startswith("subprocess.") and is_const(kw.get("shell"), True):
            self.add(node, "SAST003", "high", "subprocess com shell=True")
        elif name in ("pickle.load", "pickle.loads", "marshal.loads"):
            self.add(node, "SAST004", "high", "desserialização insegura")
        elif name in ("hashlib.md5", "hashlib.sha1"):
            self.add(node, "SAST005", "medium", f"{name} é um hash fraco")
        elif name == "yaml.load" and "Loader" not in kw and len(node.args) < 2:
            self.add(node, "SAST006", "medium", "yaml.load sem Loader seguro (usar safe_load)")
        if is_const(kw.get("verify"), False):
            self.add(node, "SAST007", "high", "verificação TLS desativada (verify=False)")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        v = node.value
        if isinstance(v, ast.Constant) and isinstance(v.value, str) and len(v.value) >= 4:
            for t in node.targets:
                n = t.id if isinstance(t, ast.Name) else t.attr if isinstance(t, ast.Attribute) else ""
                if n and SECRET_NAME.search(n):
                    self.add(node, "SAST008", "medium", f"possível segredo hardcoded em '{n}'")
        self.generic_visit(node)


def scan_source(source: str, filename: str = "<string>") -> list[Finding]:
    try:
        tree = ast.parse(source, filename)
    except (SyntaxError, ValueError) as e:
        lineno = getattr(e, "lineno", 0) or 0        
        return [Finding("PARSE", "low", filename, e.lineno or 0, "erro de sintaxe")]
    v = _Visitor(filename)
    v.visit(tree)
    return sorted(v.findings, key=lambda f: (f.line, f.rule))


def scan_path(path: pathlib.Path) -> list[Finding]:
    files = [path] if path.is_file() else [
        p for p in path.rglob("*.py") if not SKIP_DIRS.intersection(p.parts)
    ]
    out: list[Finding] = []
    for f in sorted(files):
        out += scan_source(f.read_text(encoding="utf-8", errors="replace"), str(f))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Mini SAST para Python baseado em AST")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--fail-on", choices=SEVERITY, default="high")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    findings = scan_path(pathlib.Path(a.path))
    if a.json:
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        for f in findings:
            print(f"{f.file}:{f.line} [{f.severity}] {f.rule} {f.message}")
    return 1 if any(SEVERITY[f.severity] >= SEVERITY[a.fail_on] for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())