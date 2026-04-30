#!/usr/bin/env python3
"""
56_length_extension.py — Hash Length Extension Attack
Demonstrates and performs length extension attacks against MD5/SHA-1/SHA-256/SHA-512.
Requires: pip install hashpumpy
"""

import sys

try:
    import hashpumpy
except ImportError:
    print("[-] hashpumpy not installed. Run: pip install hashpumpy")
    sys.exit(1)


# ──────────────────────────────────────────────
# Attack function
# ──────────────────────────────────────────────

def length_extension_attack(
    original_hash:  str,
    original_data:  str | bytes,
    data_to_append: str | bytes,
    key_length:     int,
) -> tuple[str, bytes]:
    """
    Perform a length extension attack.

    Parameters
    ----------
    original_hash  : Hex digest of H(secret || original_data)
    original_data  : The original message (without secret)
    data_to_append : Data to append after padding
    key_length     : Length of the secret key in bytes

    Returns
    -------
    (new_hash, new_data) where new_data = original_data || padding || data_to_append
    """
    if isinstance(original_data, str):
        original_data = original_data.encode()
    if isinstance(data_to_append, str):
        data_to_append = data_to_append.encode()

    new_hash, new_data = hashpumpy.hashpump(
        original_hash,
        original_data,
        data_to_append,
        key_length,
    )
    return new_hash, new_data


# ──────────────────────────────────────────────
# Brute-force key length
# ──────────────────────────────────────────────

def brute_force_key_length(
    original_hash:  str,
    original_data:  str | bytes,
    data_to_append: str | bytes,
    verify_fn,                          # callable(new_hash, new_data) -> bool
    max_key_len:    int = 64,
) -> tuple[int, str, bytes] | None:
    """
    Try key lengths 1..max_key_len until verify_fn returns True.

    Parameters
    ----------
    verify_fn : Function that submits (new_hash, new_data) to the server/oracle
                and returns True if accepted.

    Returns
    -------
    (key_length, new_hash, new_data) or None if not found
    """
    for key_len in range(1, max_key_len + 1):
        new_hash, new_data = length_extension_attack(
            original_hash, original_data, data_to_append, key_len
        )
        print(f"[*] Trying key_length={key_len} → hash={new_hash[:16]}...")
        if verify_fn(new_hash, new_data):
            print(f"[+] Key length found: {key_len}")
            return key_len, new_hash, new_data

    return None


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

def demo():
    import hashlib

    SECRET = b"s3cr3tkey"    # In real attack this is unknown
    KEY_LEN = len(SECRET)    # In real attack this is guessed

    original_data = b"count=10&user=alice&role=user"
    original_hash = hashlib.md5(SECRET + original_data).hexdigest()
    data_to_add   = b"&role=admin"

    print("=== Length Extension Attack Demo ===")
    print(f"  Secret (unknown to attacker) : {SECRET!r}")
    print(f"  Original data               : {original_data!r}")
    print(f"  Original hash               : {original_hash}")
    print(f"  Data to append              : {data_to_add!r}")
    print(f"  Key length guess            : {KEY_LEN}")
    print()

    new_hash, new_data = length_extension_attack(
        original_hash, original_data, data_to_add, KEY_LEN
    )

    print(f"[+] Forged hash : {new_hash}")
    print(f"[+] Forged data : {new_data!r}")

    # Verify the forged hash is valid
    expected = hashlib.md5(SECRET + new_data).hexdigest()
    if new_hash == expected:
        print("\n[✓] Verification PASSED — forged hash matches H(secret || new_data)")
    else:
        print("\n[✗] Verification FAILED")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if "--demo" in sys.argv or len(sys.argv) == 1:
        demo()
    else:
        # CLI: python 56_length_extension.py <hash> <original_data> <append_data> <key_len>
        if len(sys.argv) < 5:
            print("Usage: python 56_length_extension.py <hash> <data> <append> <key_len>")
            sys.exit(1)

        orig_hash  = sys.argv[1]
        orig_data  = sys.argv[2]
        append     = sys.argv[3]
        key_len    = int(sys.argv[4])

        new_hash, new_data = length_extension_attack(orig_hash, orig_data, append, key_len)
        print(f"New hash : {new_hash}")
        print(f"New data : {new_data!r}")
        print(f"Hex data : {new_data.hex()}")
