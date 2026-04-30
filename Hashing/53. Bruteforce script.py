#!/usr/bin/env python3
"""
53_bruteforce.py — Hash Brute-Force Script
Generates all combinations up to a given length and compares against a target hash.
"""

import hashlib
import itertools
import string
import sys

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

TARGET_HASH = "5d41402abc4b2a76b9719d911017c592"   # MD5 of "hello"
HASH_FUNC   = "md5"       # md5 | sha1 | sha256 | sha512
MAX_LENGTH  = 5           # Maximum password length to try
CHARSET     = string.ascii_lowercase  # Change as needed

# Other charset options:
# string.ascii_lowercase             → abcdefghijklmnopqrstuvwxyz
# string.ascii_letters               → a-zA-Z
# string.digits                      → 0-9
# string.ascii_lowercase + string.digits → a-z0-9
# string.printable                   → all printable ASCII


# ──────────────────────────────────────────────
# Hash function
# ──────────────────────────────────────────────

def compute_hash(plaintext: str, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(plaintext.encode("utf-8"))
    return h.hexdigest()


# ──────────────────────────────────────────────
# Brute-force engine
# ──────────────────────────────────────────────

def brute_force(target: str, algo: str, charset: str, max_len: int) -> str | None:
    total_checked = 0

    for length in range(1, max_len + 1):
        print(f"[*] Trying length {length} ({len(charset)**length:,} combinations)...")

        for combo in itertools.product(charset, repeat=length):
            candidate = "".join(combo)
            if compute_hash(candidate, algo) == target:
                print(f"\n[+] FOUND: {candidate!r}")
                print(f"[+] Hash:  {target}")
                return candidate
            total_checked += 1

        print(f"    Checked {total_checked:,} hashes so far.")

    print(f"\n[-] Not found after {total_checked:,} attempts.")
    return None


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else TARGET_HASH

    print(f"[*] Target hash : {target}")
    print(f"[*] Algorithm   : {HASH_FUNC}")
    print(f"[*] Charset     : {CHARSET!r} ({len(CHARSET)} chars)")
    print(f"[*] Max length  : {MAX_LENGTH}")
    print("-" * 50)

    result = brute_force(target, HASH_FUNC, CHARSET, MAX_LENGTH)

    if result is None:
        sys.exit(1)
