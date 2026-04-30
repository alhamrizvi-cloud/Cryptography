# Second Preimage Attack

## What is a Second Preimage Attack?
A **second preimage attack** finds a different input that produces the same hash as a known input. Unlike a collision attack (where you find any two matching inputs), here the attacker is given a specific target message and must find an alternative.

```
Given:  m1 and h = H(m1)
Goal:   Find m2 ≠ m1 such that H(m2) = H(m1)
```

---

## Three Hash Attack Comparison

```
┌─────────────────┬──────────────────────────┬───────────────────────────────┐
│ Attack          │ Given                    │ Goal                          │
├─────────────────┼──────────────────────────┼───────────────────────────────┤
│ Preimage        │ Hash h                   │ Find any m: H(m) = h          │
│ Second Preimage │ Message m1, Hash H(m1)   │ Find m2≠m1: H(m2) = H(m1)    │
│ Collision       │ Nothing                  │ Find any m1,m2: H(m1) = H(m2) │
└─────────────────┴──────────────────────────┴───────────────────────────────┘
```

**Hierarchy of hardness** (hardest to easiest to attack):
```
Preimage ≥ Second Preimage ≥ Collision
```
A hash secure against second preimage is also secure against collisions.

---

## Why Second Preimage Attacks Are Dangerous

### Document Forgery Attack
```
Alice signs:  H(contract_A) → signature
Attacker:     Finds contract_B with H(contract_B) = H(contract_A)
Result:       Alice's signature is now valid for contract_B too!
```

### Software Substitution
```
Developer releases: malware.exe with H(malware.exe) = H(legit.exe)
User:               Downloads malware.exe, hash check passes!
```

---

## Second Preimage Resistance

A hash function is **second preimage resistant** if:
- Given `m1`, it is computationally infeasible to find `m2 ≠ m1` with `H(m2) = H(m1)`
- Required security: **2^n operations** for n-bit hash (same as preimage)

---

## Long Message Second Preimage Attacks

For Merkle-Damgård constructions (MD5, SHA-1, SHA-256), long messages are more vulnerable:

```
For a message of 2^k blocks:
- Second preimage work ≈ 2^(n-k) instead of 2^n
- Herding attack exploits this

Example: SHA-256, 2^30-block message
- Normal: 2^256 operations
- Long message attack: 2^(256-30) = 2^226 operations
```

### Why? Expandable Messages
```
In MD-construction, finding intermediate collisions allows
creating alternative messages of the same block count.
This reduces the search space significantly.
```

---

## Implementation: Detecting Second Preimage Attempts

```python
import hashlib
import time

def compute_hash(data: bytes, algo: str = "sha256") -> str:
    """Compute hash using specified algorithm"""
    h = hashlib.new(algo)
    h.update(data)
    return h.hexdigest()

def check_second_preimage(original: bytes, candidate: bytes) -> bool:
    """
    Check if candidate is a second preimage of original.
    In practice, this is what attackers try to achieve.
    """
    if original == candidate:
        return False  # Must be different
    return compute_hash(original) == compute_hash(candidate)

# This should never be True for a secure hash function:
original = b"sign this contract: pay Alice $100"
forgery  = b"sign this contract: pay Bob $1000"  # Different message

print(f"Original hash: {compute_hash(original)}")
print(f"Forgery hash:  {compute_hash(forgery)}")
print(f"Second preimage? {check_second_preimage(original, forgery)}")
# → False (SHA-256 is second preimage resistant)
```

---

## Known Weaknesses

| Hash | Second Preimage Status | Notes |
|------|----------------------|-------|
| MD2 | Broken (2009) | Full second preimage attack found |
| MD4 | Broken | Practical second preimage attacks |
| MD5 | Weakened | No practical second preimage, but collision broken |
| SHA-1 | Weakened | Theoretical reduction, no practical break |
| SHA-256 | Secure | No known weaknesses |
| SHA-3 | Secure | Sponge construction inherently resistant |
| BLAKE2 | Secure | No known weaknesses |

---

## Merkle-Damgård vs Sponge (Security Implication)

### Merkle-Damgård (MD5, SHA-1, SHA-2)
```
[IV] → f(block1) → f(block2) → ... → f(blockN) → hash

Vulnerability: Long message second preimage attack
Due to: Intermediate states can be exploited
```

### Sponge (SHA-3, BLAKE3)
```
Absorb all blocks → Squeeze output
No intermediate chaining state to exploit
Better long-message second preimage resistance
```

---

## Attack Complexity Summary

| Hash | Normal 2nd Preimage | Long Message (2^40 blocks) |
|------|--------------------|-----------------------------|
| SHA-256 | 2^256 | 2^216 |
| SHA-512 | 2^512 | 2^472 |
| SHA3-256 | 2^256 | 2^256 (sponge, no reduction) |

---

## Defenses

| Defense | Against |
|---------|---------|
| Use SHA-256 or SHA-3 | Second preimage attacks in general |
| Use HMAC | Prevents extension attacks that enable second preimage |
| Sign message + context | Prevents document substitution |
| Avoid MD5/SHA-1 for signatures | These have collision weaknesses |
| Include length in message | Reduces expandable message exploits |

---

## Best Practices
- For **digital signatures**: always sign the full message, not just the hash in isolation
- Use **SHA-256 or SHA-3** — both are second preimage resistant in practice
- Avoid **MD5 and SHA-1** for any security-critical purpose
- Be aware that extremely long messages (>2^40 blocks) can have reduced security even in SHA-256
- Use **authenticated encryption** when integrity is critical
