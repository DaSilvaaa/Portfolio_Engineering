import sys
from pathlib import Path

# Adicionar a pasta src ao path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from audit import entropy_bits, rate


def test_entropy_empty():
    assert entropy_bits("") == 0.0


def test_entropy_lowercase_only():
    # 8 caracteres apenas em minúsculas (pool = 26)
    bits = entropy_bits("abcdefgh")
    assert round(bits, 1) == 37.6
    assert rate(bits) == "fraca"


def test_entropy_complex_password():
    # Minúsculas + maiúsculas + números + símbolos (pool = 94)
    bits = entropy_bits("P@ssw0rd2026!#")
    assert bits > 80.0
    assert rate(bits) == "muito forte"


def test_ratings():
    assert rate(30.0) == "fraca"
    assert rate(50.0) == "razoavel"
    assert rate(70.0) == "forte"
    assert rate(90.0) == "muito forte"
