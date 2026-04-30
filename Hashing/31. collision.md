# Collision Attack

## What is a Collision Attack?
A **collision attack** finds two different inputs that produce the same hash output. Unlike preimage attacks, the attacker is free to choose **both** inputs — making collisions significantly easier to find than preimages.

```
Goal: Find m1 ≠ m2 such that H(m1) = H(m2)
```

---

## Birthday Problem (Why Collisions Are Easier)

The birthday paradox explains why finding collisions only requires ~√(2^n) = **2^(n/2)** operations:

```
n-bit hash → find collision in ~2^(n/2) attempts

SHA-256 (256-bit): collision requires ~2^128 operations
SHA-1  (160-bit): collision requires ~2^80 operations (broken!)
MD5    (128-bit): collision requires ~2^64 operations (trivially broken!)
```

**Compare to preimage**: requires 2^n operations — collision is 2^(n/2) times easier!

---

## Birthday Paradox Intuition

```
In a room of 23 people → 50% chance two share a birthday
In a room of 57 people → 99% chance two share a birthday

365 days → need only √365 ≈ 23 people for 50% collision

Same math: 2^128 hashes → need only 2^64 hashes for 50% collision
```

---

## Types of Collisions

### Classic Collision
```
H(m1) = H(m2)  where m1 ≠ m2
Attacker controls both m1 and m2
```

### Chosen-Prefix Collision
```
H(prefix1 || suffix1) = H(prefix2 || suffix2)
Where prefix1 and prefix2 are chosen by attacker
More powerful — enables practical attacks
```

### Identical-Prefix Collision
```
H(prefix || suffix1) = H(prefix || suffix2)
Same prefix, different suffixes — used in early MD5 attacks
```

---

## Real-World Collision Attacks

### MD5 — Completely Broken (1996–2008)
```
2004: Wang et al. found MD5 collisions in hours
2008: Researchers used MD5 collisions to create a rogue CA certificate
      (trusted HTTPS certificate for any domain!)

Example collision (same MD5 hash):
File 1: d131dd02c5e6eec4693d9a0698aff95c ...
File 2: d131dd02c5e6eec4693d9a0698aff95c ...
MD5:    79054025255fb1a26e4bc422aef54eb4 (SAME!)
```

### SHA-1 — Broken (2017)
```
Google's SHAttered attack:
- First practical SHA-1 collision found in 2017
- Two different PDF files with same SHA-1 hash
- Cost: ~$110,000 in cloud computing (at 2017 prices)
- PDF 1: shattered-1.pdf → SHA-1: 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
- PDF 2: shattered-2.pdf → SHA-1: 38762cf7f55934b34d179ae6a4c80cadccbb7f0a
```

### SHA-256 — Not Broken
```
No practical collision found
2^128 operations required → physically infeasible
```

---

## Demonstrating the Danger

### Rogue CA Certificate Attack (MD5)
```
1. Attacker requests cert for evil.com from legitimate CA
2. CA signs: H(evil.com cert) → signature  
3. Attacker finds: cert_A (for evil.com) and cert_B (rogue CA)
   such that H(cert_A) = H(cert_B)
4. CA's signature on cert_A is now valid for cert_B
5. Attacker has a trusted CA cert — can sign any HTTPS cert!
```

### Document Forgery with MD5
```python
# Conceptually: two .exe files with same MD5
# Developer publishes MD5 of legitimate_app.exe
# Attacker prepares malware.exe with SAME MD5
# Users verify hash — it matches! But it's malware.
```

---

## Python: Birthday Attack Simulation

```python
import hashlib
import random

def truncated_hash(data: bytes, bits: int) -> int:
    """Simulate a weak n-bit hash by truncating SHA-256"""
    h = hashlib.sha256(data).digest()
    mask = (1 << bits) - 1
    return int.from_bytes(h[:4], 'big') & mask

def birthday_attack(hash_bits: int = 16):
    """
    Demonstrate birthday attack on a weak truncated hash.
    Expected attempts ≈ sqrt(2^bits) = 2^(bits/2)
    """
    seen = {}
    attempts = 0
    
    while True:
        # Random message
        msg = random.randbytes(8)
        h = truncated_hash(msg, hash_bits)
        attempts += 1
        
        if h in seen and seen[h] != msg:
            print(f"Collision found after {attempts} attempts!")
            print(f"m1: {seen[h].hex()}")
            print(f"m2: {msg.hex()}")
            print(f"Hash: {h:0{hash_bits//4}x}")
            return attempts
        
        seen[h] = msg

# Should find collision in ~256 attempts for 16-bit hash (2^8)
birthday_attack(16)
```

---

## Collision Resistance Status

| Hash | Bits | Collision Work | Status |
|------|------|---------------|--------|
| MD4 | 128 | Trivial | ❌ Completely broken |
| MD5 | 128 | Minutes | ❌ Broken |
| SHA-1 | 160 | ~$110k | ❌ Broken (2017) |
| SHA-256 | 256 | 2^128 | ✅ Secure |
| SHA-512 | 512 | 2^256 | ✅ Secure |
| SHA3-256 | 256 | 2^128 | ✅ Secure |
| BLAKE2b | 512 | 2^256 | ✅ Secure |
| BLAKE3 | 256 | 2^128 | ✅ Secure |

---

## Defenses Against Collision Attacks

| Defense | Description |
|---------|-------------|
| Use SHA-256 or SHA-3 | Collision requires 2^128 ops — infeasible |
| Avoid MD5 and SHA-1 | For any security purpose |
| Use digital timestamps | Detect retroactive forgery |
| Include unique nonces | Prevent reuse of collision pairs |
| Use HMAC | Adds secret key, prevents offline collision searching |

---

## Implications for Digital Signatures

```
If H has collisions:
  Sign(H(legit_doc)) → sig
  Attacker finds: H(malicious_doc) = H(legit_doc)
  → sig is valid for malicious_doc!

Solution: Use collision-resistant hashes (SHA-256+)
```

---

## Best Practices
- **Never use MD5 or SHA-1** for digital signatures, certificates, or security
- Use **SHA-256 or SHA-3** for all new applications
- For critical applications: use **SHA-384 or SHA-512** for extra margin
- Check **certificate/hash algorithm** in all third-party dependencies
- When storing hashes, include the **algorithm identifier** so you can upgrade later
