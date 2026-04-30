# Key Stretching

## What is Key Stretching?
**Key stretching** is a technique that takes a weak key (like a short password) and makes it computationally expensive to verify by running it through many iterations of a hash function or a memory-hard algorithm. This forces attackers to spend enormous time/resources when brute-forcing.

```
Weak Password → [Many Iterations / Memory-hard ops] → Strong Derived Key
```

---

## Why Key Stretching?

### The Problem: Passwords are Weak
- Users choose short, predictable passwords
- A GPU can try billions of MD5/SHA hashes per second
- Without stretching: cracking is trivial

### The Solution: Make Each Guess Expensive
```
Without stretching: 1 billion guesses/sec
With stretching (cost=12): ~1,000 guesses/sec  ← 1,000,000× slower
```

---

## How Key Stretching Works

### Simple Iteration (PBKDF2 model)
```
derived_key = password
for i in range(iterations):
    derived_key = HMAC(derived_key + salt)
return derived_key
```

### Memory-Hard (Argon2/scrypt model)
```
1. Fill large memory buffer (e.g., 64 MB)
2. Make random-access reads over memory
3. Output depends on memory contents
→ Cannot be parallelized efficiently on GPU/ASIC
```

---

## Key Stretching Algorithms

### PBKDF2 (Password-Based Key Derivation Function 2)
```python
import hashlib

dk = hashlib.pbkdf2_hmac(
    'sha256',           # hash algorithm
    b'password',        # password
    b'salt',            # salt
    iterations=600000,  # OWASP 2023 recommendation
    dklen=32            # output length
)
```
- Standard: RFC 8018
- **Not memory-hard** — vulnerable to GPU attacks
- Iterations: use 600,000+ for SHA-256

### bcrypt
```python
import bcrypt
hashed = bcrypt.hashpw(b"password", bcrypt.gensalt(rounds=12))
# 2^12 = 4096 iterations of EksBlowfish
```
- Built-in salt
- Work factor: adjustable (2^cost iterations)

### scrypt
```python
import hashlib
dk = hashlib.scrypt(b"password", salt=b"salt", n=16384, r=8, p=1)
# n=16384 → 16 MB RAM required
```
- Both CPU and memory hard

### Argon2 ✅ (Recommended)
```python
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash = ph.hash("password")
```
- Time + memory + parallelism costs
- Most modern and secure

---

## Iteration Count Guide

| Algorithm | Minimum Iterations | OWASP 2023 Recommendation |
|-----------|-------------------|--------------------------|
| PBKDF2-SHA1 | 720,000 | 1,300,000 |
| PBKDF2-SHA256 | 310,000 | 600,000 |
| PBKDF2-SHA512 | 120,000 | 210,000 |
| bcrypt | cost=10 | cost=12 |
| scrypt | N=2^14 | N=2^17 |
| Argon2id | m=19MB,t=2 | m=64MB,t=3 |

---

## Performance vs Security Trade-off

```
Iterations: 1        → 0.001ms per hash → Insecure (billions/sec feasible)
Iterations: 1,000    → 1ms per hash     → Weak
Iterations: 100,000  → 100ms per hash   → Acceptable
Iterations: 600,000  → 600ms per hash   → Good (PBKDF2-SHA256)
Cost factor 12       → ~400ms           → Good (bcrypt)
```

**Target: 100–500ms on your server hardware**

---

## Key Stretching in Encryption

Key stretching is also used to derive encryption keys from passwords:

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64, os

password = b"user_password"
salt = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=600000,
)
key = base64.urlsafe_b64encode(kdf.derive(password))
fernet = Fernet(key)

# Now use fernet for encryption/decryption
encrypted = fernet.encrypt(b"secret data")
```

---

## Attack Resistance Comparison

| Algorithm | CPU Attack | GPU Attack | ASIC Attack |
|-----------|-----------|-----------|------------|
| SHA-256 (no stretching) | Trivial | Trivial | Trivial |
| PBKDF2 (600k iter) | Hard | Moderate | Moderate |
| bcrypt (cost 12) | Hard | Hard | Hard |
| scrypt (N=65536) | Hard | Very Hard | Hard |
| Argon2id (64MB,t=3) | Hard | Very Hard | Very Hard |

---

## Best Practices
- Always use dedicated **password hashing libraries** (bcrypt, Argon2)
- **Benchmark on your hardware** — tune to reach ~300ms
- **Increase cost factor** annually as hardware improves
- For encryption keys: use **PBKDF2 or Argon2** with sufficient iterations
- Never use raw MD5/SHA for passwords, even with high iteration counts — use PBKDF2 or better
- Store cost parameters with the hash so future upgrades are possible
