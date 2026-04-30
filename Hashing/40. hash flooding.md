# Hash Flooding (HashDoS)

## What is Hash Flooding?
**Hash flooding** (also called **HashDoS**) is a Denial-of-Service attack that exploits hash table collision behavior. By sending many inputs that all hash to the same bucket, an attacker degrades hash table operations from O(1) to O(n), causing CPU exhaustion.

```
Normal hash table lookup:  O(1) average
Under hash flooding:       O(n) — server hangs!
```

---

## How Hash Tables Work (Normal)

```
HashMap inserts by:
1. Compute hash(key) → bucket index
2. Insert into that bucket (linked list if collision)

Normal case: ~1 item per bucket → O(1) lookup
Worst case:  all items in 1 bucket → O(n) lookup
```

---

## The Attack

```
Attacker finds (or crafts) thousands of strings that all
hash to the same bucket in the server's hash table:

"Aa", "BB", "C#" ... all → hash = 2134 (same bucket!)

Server receives HTTP POST with 100,000 such key=value pairs
Server builds HashMap → all 100,000 keys in ONE bucket
Every insert/lookup → O(n) → O(n²) total → CPU 100% → DoS!
```

---

## Vulnerable Scenario

```
HTTP POST request body:
Aa=1&BB=2&C%23=3& ... (100,000 crafted key=value pairs)

PHP/Ruby/Java/Python parse this → create HashMap
Each insertion hits the same bucket:
O(1 + 2 + 3 + ... + 100000) = O(n²/2) ≈ 5 billion operations

1 attacker with 1 request → server pegged at 100% CPU
```

---

## Affected Languages/Frameworks (2011 Disclosure)

| Language | Vulnerable Version | Fixed In |
|----------|--------------------|---------|
| PHP | < 5.3.9 | 5.3.9 |
| Java | < JDK 7u6 | JDK 7u6 |
| Python | < 3.3 | 3.3 (hash randomization) |
| Ruby | < 1.9.3-p327 | 1.9.3-p327 |
| ASP.NET | < 4.5 | 4.5 |
| Node.js | Various | Added `--hash-seed` |

---

## Code Examples

### Demonstrating the Problem (Python < 3.3)
```python
# Before Python 3.3: hash() was deterministic
# Attacker could precompute colliding strings

# In Python 3.3+: PYTHONHASHSEED randomizes hash()
# python -c "print(hash('hello'))"  → different each run!

# Simulate vulnerable behavior:
import sys

def naive_hash(s: str, table_size: int = 8) -> int:
    """Simplified hash with no randomization"""
    h = 0
    for c in s:
        h = (h * 31 + ord(c)) % table_size
    return h

# Crafted collision strings:
strings = ["Aa", "BB", "C#"]  # All hash to same bucket in Java HashMap

for s in strings:
    print(f"hash('{s}') = {naive_hash(s)}")
# All print the same bucket!
```

### Vulnerable Server (Flask — hypothetical)
```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/vulnerable', methods=['POST'])
def vulnerable():
    # ❌ Parsing all POST params into dict — vulnerable if no limit
    data = request.form.to_dict()  # Attacker sends 100k crafted keys
    return str(len(data))
```

### Protected Server
```python
from flask import Flask, request

app = Flask(__name__)
MAX_PARAMS = 1000

@app.route('/protected', methods=['POST'])
def protected():
    # ✅ Limit number of parameters
    if len(request.form) > MAX_PARAMS:
        return "Too many parameters", 400
    data = request.form.to_dict()
    return str(len(data))
```

---

## Fix 1: Hash Randomization (Main Defense)

```python
# Python 3.3+ uses PYTHONHASHSEED by default
# Every process restart = different hash seed
# Attacker can't precompute colliding strings

import os
print(os.environ.get('PYTHONHASHSEED', 'random'))  # 'random' = randomized

# Force randomization:
# PYTHONHASHSEED=random python server.py

# Java fix: use randomized HashMap (JDK 7u6+)
# HashMap now randomizes hash seeds per-instance
```

---

## Fix 2: Use Collision-Resistant Hash (SipHash)

```python
# Python 3.4+ uses SipHash-2-4 for string/bytes hashing
# SipHash: fast, but keyed — attacker can't predict collisions without key

import hashlib

# SipHash via ctypes (Python internals use it)
# Just use Python 3.4+ and it's automatic for dict keys

# Go uses AES-based hash randomization
# Rust uses SipHash by default in HashMap
```

### SipHash Implementation
```python
# pip install siphash
import siphash

key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
h = siphash.SipHash_2_4(key, b"hello").hash()
# Attacker doesn't know key → can't compute collisions
```

---

## Fix 3: Input Limits

```python
# Limit input size and parameter count at every layer:

# Nginx config
# client_max_body_size 1m;
# large_client_header_buffers 4 8k;

# Application layer
MAX_BODY = 1_000_000   # 1 MB
MAX_KEYS = 1_000       # 1000 keys max

def parse_safely(body: bytes) -> dict:
    if len(body) > MAX_BODY:
        raise ValueError("Request too large")
    params = parse_qs(body)
    if len(params) > MAX_KEYS:
        raise ValueError("Too many parameters")
    return params
```

---

## Fix 4: Use Tree Maps Instead of Hash Maps

```java
// Java: Use TreeMap for untrusted keys (O(log n) worst case vs O(n))
// TreeMap uses red-black tree — no hash collision issue
Map<String, String> params = new TreeMap<>(request.getParameterMap());
// O(n log n) worst case instead of O(n²)
```

---

## Defense Summary

| Defense | Effectiveness | Complexity |
|---------|--------------|-----------|
| Hash randomization (Python 3.3+, Java 7u6+) | High | None (built-in) |
| SipHash for hash tables | High | Low |
| Input size limits | High | Low |
| Parameter count limits | High | Low |
| Rate limiting requests | Medium | Low |
| TreeMap instead of HashMap | Medium | Low |
| WAF rules for large POST bodies | Medium | Medium |

---

## Best Practices
- **Update your runtime** — Python 3.3+, Java 7u6+, Ruby 1.9.3-p327 all fix this
- **Limit POST body size** at the web server level (nginx, Apache)
- **Limit parameter count** in your application
- Use **rate limiting** to slow repeated large requests
- Prefer **SipHash** or randomized hashing for hash tables processing untrusted input
- Never use a deterministic, predictable hash for data structures that accept external input
