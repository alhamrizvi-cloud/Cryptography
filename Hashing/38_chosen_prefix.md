# Chosen-Prefix Collision Attack

## What is a Chosen-Prefix Attack?
A **chosen-prefix collision attack** is a powerful variant of a collision attack where the attacker can choose **two arbitrary prefixes** and compute suffixes that make both documents hash to the same value.

```
Given: prefix1, prefix2 (chosen by attacker)
Find:  suffix1, suffix2 such that:
       H(prefix1 || suffix1) = H(prefix2 || suffix2)
```

This is more dangerous than identical-prefix collisions because the attacker controls the meaningful content of both documents.

---

## Comparison of Collision Types

| Type | Control | Difficulty | Danger |
|------|---------|-----------|--------|
| Identical-prefix | Same prefix, find any 2 suffixes | Easiest | Low |
| Chosen-prefix | Choose both prefixes freely | Harder | **Very High** |
| Second preimage | Fixed target message | Hardest | Extremely High |

---

## Why Chosen-Prefix is Devastating

### Rogue CA Attack (2008, MD5)
```
Attacker wants: A CA certificate (signs any HTTPS cert)

Step 1: Get CA to sign a legit cert for evil.com
        prefix1 = legit cert for evil.com

Step 2: Construct a rogue CA cert
        prefix2 = rogue CA cert

Step 3: Find suffix1, suffix2 such that:
        MD5(prefix1 || suffix1) = MD5(prefix2 || suffix2)

Step 4: CA signs (prefix1 || suffix1) → signature
        Signature is now VALID for (prefix2 || suffix2)
        → Attacker has a trusted CA certificate!
        → Can issue valid HTTPS certs for any domain!
```

### PGP Key Forgery (2019, SHA-1)
```
Researchers created two PGP keys with different identities
but the same SHA-1 fingerprint — allowing signature transfer
```

---

## Technical Details (MD5 Chosen-Prefix)

```
Approach: "Near-collision blocks"

1. Compute intermediate hash state after prefix1 and prefix2
   State1 = H_state(prefix1)
   State2 = H_state(prefix2)

2. Find "near-collision blocks" that bring states closer
   (Using differential cryptanalysis on the compression function)

3. Apply final identical-prefix collision blocks
   to make states exactly equal

4. Result: H(prefix1 || near-collision || collision) =
           H(prefix2 || near-collision || collision)
```

---

## Timeline of Chosen-Prefix Attacks

| Year | Hash | Researchers | Cost |
|------|------|------------|------|
| 2007 | MD5 | Stevens et al. | Hours on PC |
| 2008 | MD5 | Sotirov et al. | Used for Rogue CA |
| 2019 | SHA-1 | Leurent & Peyrin | ~$45,000 GPU |
| 2020 | SHA-1 | Improved | ~$11,000 GPU |
| — | SHA-256 | None known | — |

---

## Detection Example

```python
import hashlib

def has_same_hash(doc1: bytes, doc2: bytes, algo="sha256") -> bool:
    """
    Check if two different documents share a hash.
    If True with MD5/SHA1, could indicate chosen-prefix attack.
    """
    if doc1 == doc2:
        return False
    h = hashlib.new(algo)
    h1 = hashlib.new(algo, doc1).hexdigest()
    h2 = hashlib.new(algo, doc2).hexdigest()
    return h1 == h2

# Verify your certificate pipeline uses SHA-256, not MD5/SHA-1
import ssl, socket

def check_cert_hash_algo(hostname: str) -> str:
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, 443))
        cert = s.getpeercert()
        return cert.get('signatureAlgorithm', 'unknown')

algo = check_cert_hash_algo("example.com")
print(f"Certificate signed with: {algo}")
# Should be: sha256WithRSAEncryption (not sha1WithRSAEncryption!)
```

---

## Defense Against Chosen-Prefix Attacks

| Defense | How It Helps |
|---------|-------------|
| Use SHA-256/SHA-3 | No known chosen-prefix attacks |
| Include timestamps in signed data | Old collision pairs invalid |
| Use HMAC | Secret key prevents offline search |
| Certificate Transparency (CT logs) | Detect rogue CA certs |
| Use randomized nonces in protocols | Can't precompute collision |
| Avoid MD5/SHA-1 completely | Eliminates vulnerable algorithms |

---

## Best Practices
- **Never use MD5 or SHA-1** in any signature, certificate, or integrity check
- Check that all TLS certificates use **SHA-256 or better**
- For code signing and document signing: use **SHA-384 or SHA-512**
- Implement **Certificate Transparency** monitoring
- When designing protocols: include **random nonces** that prevent precomputed attacks
