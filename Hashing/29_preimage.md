# Preimage Attack

## What is a Preimage Attack?
A **preimage attack** on a hash function attempts to find an input `m` such that `hash(m) = h` for a given target hash `h`. In other words: given a hash output, find **any** input that produces it.

```
Given:  h = H(?)
Goal:   Find any m such that H(m) = h
```

---

## Types of Hash Attacks

| Attack | Given | Find |
|--------|-------|------|
| **Preimage** | hash `h` | any `m` where `H(m) = h` |
| **Second Preimage** | `m1` and `H(m1)` | `m2 ≠ m1` where `H(m2) = H(m1)` |
| **Collision** | nothing | any `m1, m2` where `H(m1) = H(m2)` |

---

## Preimage Resistance

A hash function is **preimage resistant** (one-way) if:
- Given `h`, it is computationally infeasible to find any `m` such that `H(m) = h`
- Expected work: **2^n operations** for an n-bit hash

```
SHA-256: 2^256 operations required (infeasible)
MD5:     2^128 theoretically, but weaknesses exist
```

---

## How Preimage Attacks Work

### Brute Force
```python
target_hash = "5f4dcc3b5aa765d61d8327deb882cf99"  # MD5 of "password"

# Try all possibilities
for candidate in all_possible_strings():
    if md5(candidate) == target_hash:
        print(f"Found preimage: {candidate}")
        break
```

### Time Complexity
```
For an n-bit hash:
- Brute force requires O(2^n) hash computations
- MD5 (128-bit):    2^128 ≈ 3.4 × 10^38 operations
- SHA-256 (256-bit): 2^256 ≈ 1.2 × 10^77 operations
```

---

## Real-World Preimage Attacks

### MD4 — Broken
- Preimage attack in 2 rounds found (theoretical complexity reduced)

### MD5 — Weakened but no practical preimage
- No practical preimage attack exists yet
- But collision attacks are trivial → use SHA-256 instead

### SHA-1 — Weakened
- Theoretical preimage reduced to 2^160 but no practical break

### SHA-256 / SHA-3 — No known preimage attack
- Currently considered preimage resistant

---

## Preimage Attack in Password Cracking Context

When an attacker steals a database of hashes:
```
Target: e10adc3949ba59abbe56e057f20f883e  (MD5 hash)

Attack options:
1. Brute force:     try all passwords until match
2. Dictionary:      try common passwords
3. Rainbow table:   lookup precomputed preimage table
4. Rule-based:      apply mutations to wordlist

Found preimage: "123456"  ✓
```

This is the **core goal of password cracking** — finding a preimage.

---

## Hellman's Time-Memory Trade-off

A classic approach to preimage attacks:
```
Precompute many (input → hash) pairs and store in a table
Trade storage space for faster lookups

Rainbow tables use this technique with chain compression
```

---

## Python: Simulating a Simple Preimage Attack

```python
import hashlib

def simple_preimage_attack(target_hash: str, wordlist: list) -> str | None:
    """Attempt to find a preimage via dictionary attack"""
    for word in wordlist:
        attempt = hashlib.md5(word.encode()).hexdigest()
        if attempt == target_hash:
            return word
    return None

# Example
target = hashlib.md5(b"hello").hexdigest()  # "5d41402abc4b2a76b9719d911017c592"
wordlist = ["hi", "hello", "world", "test"]

result = simple_preimage_attack(target, wordlist)
print(f"Preimage found: {result}")  # "hello"
```

---

## Preimage Attack Complexity

| Hash | Bits | Theoretical Work | Status |
|------|------|-----------------|--------|
| MD5 | 128 | 2^128 | No practical preimage |
| SHA-1 | 160 | 2^160 | No practical preimage |
| SHA-256 | 256 | 2^256 | Secure |
| SHA-512 | 512 | 2^512 | Secure |
| SHA3-256 | 256 | 2^256 | Secure |

---

## Defenses Against Preimage Attacks

| Defense | How It Helps |
|---------|-------------|
| Use SHA-256+ | Computationally infeasible to brute force |
| Salt passwords | Defeats rainbow table lookups |
| Use bcrypt/Argon2 | Makes each guess extremely slow |
| Long hash outputs | More bits = exponentially more work |

---

## Preimage Resistance vs One-Way Function

```
Preimage resistant ≡ One-way function
A hash H is preimage resistant if:
  ∀h, it is hard to find m such that H(m) = h
  
Formally: no polynomial-time algorithm can compute the preimage
          with non-negligible probability
```

---

## Best Practices
- Always use **preimage resistant** hash functions (SHA-256, SHA-3)
- For passwords: add **salt + use a KDF** (bcrypt, Argon2)
- Never use MD5 or SHA-1 for security-sensitive purposes
- The preimage resistance of a hash is why it can be used as a **commitment scheme**
