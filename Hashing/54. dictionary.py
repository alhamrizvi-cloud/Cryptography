#!/usr/bin/env python3
"""
54_dictionary.py — Dictionary-Based Hash Cracker
Reads a wordlist and checks each word (with optional rules/mutations) against target hashes.
"""

import hashlib
import sys
import os
from itertools import product

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

TARGET_HASHES = {
    "5d41402abc4b2a76b9719d911017c592",   # MD5("hello")
    "aaf4c61ddcc5e8a2dabede0f3b482cd9",   # SHA1("hello")
}

HASH_FUNC  = "md5"                        # md5 | sha1 | sha256 | sha512
WORDLIST   = "/usr/share/wordlists/rockyou.txt"   # Change path as needed
APPLY_RULES = True                        # Toggle mutation rules


# ──────────────────────────────────────────────
# Hash function
# ──────────────────────────────────────────────

def compute_hash(plaintext: str, algo: str) -> str:
    h = hashlib.new(algo)
    h.update(plaintext.encode("utf-8", errors="replace"))
    return h.hexdigest()


# ──────────────────────────────────────────────
# Mutation Rules
# ──────────────────────────────────────────────

def mutate(word: str):
    """Yield common transformations of a word."""
    yield word                          # original
    yield word.lower()
    yield word.upper()
    yield word.capitalize()
    yield word + "1"
    yield word + "123"
    yield word + "!"
    yield word + "2024"
    yield word + "2025"
    yield "1" + word
    # Leetspeak
    leet = word.replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0")
    yield leet
    yield leet.capitalize()


# ──────────────────────────────────────────────
# Cracker
# ──────────────────────────────────────────────

def crack(targets: set, algo: str, wordlist_path: str, use_rules: bool) -> dict:
    """Return dict of {hash: plaintext} for cracked hashes."""
    cracked = {}
    remaining = set(targets)
    count = 0

    if not os.path.exists(wordlist_path):
        print(f"[-] Wordlist not found: {wordlist_path}")
        sys.exit(1)

    print(f"[*] Cracking {len(targets)} hash(es) with {wordlist_path}")
    print(f"[*] Algorithm : {algo} | Rules: {use_rules}")
    print("-" * 50)

    with open(wordlist_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if not remaining:
                break

            word = line.rstrip("\n")
            candidates = mutate(word) if use_rules else [word]

            for candidate in candidates:
                h = compute_hash(candidate, algo)
                if h in remaining:
                    cracked[h] = candidate
                    remaining.discard(h)
                    print(f"[+] CRACKED: {h} → {candidate!r}")

            count += 1
            if count % 500_000 == 0:
                print(f"    Tried {count:,} words, {len(remaining)} hash(es) remaining...")

    return cracked


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == "__main__":
    # Support reading hashes from file: python 54_dictionary.py hashes.txt
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fh:
            targets = {line.strip() for line in fh if line.strip()}
    else:
        targets = TARGET_HASHES

    results = crack(targets, HASH_FUNC, WORDLIST, APPLY_RULES)

    print("\n=== Results ===")
    for h, p in results.items():
        print(f"  {h}  →  {p}")

    not_cracked = targets - set(results.keys())
    if not_cracked:
        print(f"\n[-] Not cracked ({len(not_cracked)}):")
        for h in not_cracked:
            print(f"  {h}")
