import math
import string
import sys

def entropy_bits(pw: str) -> float:
    pool = 0
    pool += 26 if any(c in string.ascii_lowercase for c in pw) else 0
    pool += 26 if any(c in string.ascii_uppercase for c in pw) else 0
    pool += 10 if any(c in string.digits for c in pw) else 0
    pool += 32 if any(c in string.punctuation for c in pw) else 0
    return len(pw) * math.log2(pool) if pool else 0.0

def rate(bits: float) -> str:
    return "fraca" if bits < 40 else "razoavel" if bits < 60 else "forte" if bits < 80 else "muito forte"

if __name__ == "__main__":
    for line in sys.stdin:
        pw = line.rstrip("\n")
        bits = entropy_bits(pw)
        print(f"{len(pw):>3} chars | {bits:6.1f} bits | {rate(bits)}")
