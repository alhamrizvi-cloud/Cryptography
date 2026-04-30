# Collision Attack (Advanced)

## Overview
A **collision attack** exploits hash function weaknesses to find two different inputs producing the same hash — faster than the birthday bound of 2^(n/2). See `31_collision.md` for fundamentals. This file covers advanced techniques and real exploits.

---

## Differential Cryptanalysis (The Core Technique)

Most collision attacks use **differential cryptanalysis**:

```
1. Choose input difference ΔM = M1 ⊕ M2
2. Track how this difference propagates through hash rounds
3. Find a "differential path" where differences cancel out
4. Result: H(M1) = H(M2) despite M1 ≠ M2
```

```
M1: [block]  →  [round1]  →  [round2]  →  [round64]  →  hash
     ΔM ↓          ↓ diff          ↓ diff        ↓ → 0
M2: [block]  →  [round1'] →  [round2'] →  [round64'] →  same hash!
```

---

## Notable Real Attacks

### MD5 (Wang et al., 2004)
```
- Found collisions in < 1 hour on a PC
- Two 1024-bit messages with identical MD5
- Later: < 1 second on modern hardware

Example (actual MD5 collision):
d131dd02c5e6eec4693d9a0698aff95c 2fcab58712467eab4004583eb8fb7f89
55ad340609f4b30283e488832571415a 085125e8f7cdc99fd91dbdf280373c5b
d8823e3156348f5bae6dacd436c919c6 dd53e2b487da03fd02396306d248cda0
e99f33420f577ee8ce54b67080a80d1e c69821bcb6a8839396f9652b6ff72a70

d131dd02c5e6eec4693d9a0698aff95c 2fcab50712467eab4004583eb8fb7f89
55ad340609f4b30283e4888325f1415a 085125e8f7cdc99fd91dbd7280373c5b
d8823e3156348f5bae6dacd436c919c6 dd53e2b487da03fd02396306d248cda0
e99f33420f577ee8ce54b67080280d1e c69821bcb6a8839396f965ab6ff72a70

Both have MD5: 79054025255fb1a26e4bc422aef54eb4
```

### SHA-1 SHAttered (Google, 2017)
```
- First practical SHA-1 collision
- Two different PDF files, same SHA-1
- Cost: ~9.2 quintillion SHA-1 computations
- ~$110,000 in cloud compute at 2017 prices

Files: shattered-1.pdf and shattered-2.pdf
SHA-1: 38762cf7f55934b34d179ae6a4c80cadccbb7f0a (SAME for both!)
```

### Chosen-Prefix Collision (MD5, 2008)
```
Used to forge a rogue CA certificate:
1. Obtained legit cert for evil.com
2. Found: H(evil.com cert) = H(rogue_CA cert)  ← collision!
3. CA's signature on evil.com cert → valid for rogue CA cert
4. Could sign ANY HTTPS certificate → man-in-the-middle any site
```

---

## Chosen-Prefix vs Identical-Prefix

```
Identical-prefix collision:
  H(prefix || suffix1) = H(prefix || suffix2)
  Attacker picks prefix before collision search

Chosen-prefix collision (more powerful):
  H(prefix1 || suffix1) = H(prefix2 || suffix2)
  Attacker picks BOTH prefixes (e.g., two different documents)
  → Can forge signatures on arbitrary documents
```

---

## Detecting Collision Attacks

```python
import hashlib

def detect_collision_attempt(files: list[bytes]) -> dict:
    """Check if any two files share a hash (possible collision)"""
    hashes = {}
    collisions = []
    
    for i, content in enumerate(files):
        h = hashlib.sha256(content).hexdigest()
        if h in hashes:
            collisions.append({
                "file1": hashes[h],
                "file2": i,
                "hash": h
            })
        hashes[h] = i
    
    return {
        "total_files": len(files),
        "collisions_found": len(collisions),
        "details": collisions
    }
```

---

## Current Status of Hash Functions

| Hash | Collision Attack | Practical? | Recommendation |
|------|-----------------|-----------|----------------|
| MD5 | Yes (seconds) | ✅ Yes | ❌ Never use |
| SHA-1 | Yes ($110k) | ✅ Yes | ❌ Deprecated |
| SHA-256 | Theoretical only | ❌ No | ✅ Use this |
| SHA-3 | None known | ❌ No | ✅ Excellent |
| BLAKE2 | None known | ❌ No | ✅ Fast option |

---

## Defense
- **Use SHA-256 or SHA-3** for all new systems
- **Migrate away from MD5/SHA-1** immediately
- Use **HMAC** (adds secret key — attacker can't search for collisions offline)
- For code signing: use **SHA-256 minimum**, prefer SHA-384/512
- Check certificate/TLS configurations for SHA-1 usage
