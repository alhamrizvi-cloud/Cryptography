# Rainbow Tables

## What are Rainbow Tables?
**Rainbow tables** are precomputed tables mapping hash values back to their original inputs. They use a time-memory trade-off — spend time computing once, then look up hashes instantly.

```
hash → plaintext lookup
"5f4dcc3b..." → "password"  (instant!)
```

---

## How Rainbow Tables Work

### Naive Lookup Table (Too Large)
```
Store every (password → hash) pair
Problem: Would require petabytes for full coverage
```

### Rainbow Chain Solution
```
Reduce function R converts hash back to a candidate password
(R is NOT the inverse of H — it maps hash space → password space)

password → H → hash → R → password → H → hash → R → ... → hash
   p0    →   →  h0  →   →   p1     →   →  h1  →   → ... →  hk

Store only: (p0, hk) — the start and end of each chain!
```

### Lookup Process
```
Given target hash ht:
1. Apply R to ht → get candidate → hash it → check if in table endpoint
2. If not found, apply R again, hash again, check
3. If found, regenerate the chain from stored start point
4. Walk chain until original hash is found → return the plaintext
```

---

## Rainbow Table Stats

| Hash | Charset | Length | Table Size | Coverage |
|------|---------|--------|-----------|---------|
| MD5 | a-z0-9 | 1-8 | ~64 GB | ~99.9% |
| SHA-1 | a-z0-9 | 1-8 | ~160 GB | ~99% |
| SHA-256 | a-z0-9 | 1-7 | ~300 GB | ~80% |
| bcrypt | Any | Any | Infeasible | ~0% |

---

## Why Salt Defeats Rainbow Tables

```
Without salt:
  H("password") = 5f4dcc3b...  ← precomputed in table!

With salt "xK9mP2":
  H("password" + "xK9mP2") = a3f71c...  ← NOT in any precomputed table
  H("password" + "qL5nR8") = 9b2e5f...  ← different salt = different hash

Attacker would need a separate rainbow table per salt — infeasible!
```

---

## Tools & Resources

```bash
# RainbowCrack tool
rcrack . -h 5f4dcc3b5aa765d61d8327deb882cf99

# Online rainbow table lookups (MD5/SHA1 only)
# https://crackstation.net
# https://hashes.com
# https://md5decrypt.net
```

---

## Defense
- **Always salt** passwords (renders rainbow tables useless)
- Use **bcrypt/Argon2** (built-in salting + key stretching)
- Use **long random salts** (≥ 16 bytes)
- Never store **unsalted hashes**
