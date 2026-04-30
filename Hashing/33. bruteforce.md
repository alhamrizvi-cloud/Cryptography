# Brute Force Attack

## What is a Brute Force Attack?
A **brute force attack** systematically tries every possible combination of characters until the correct password, key, or input is found. It requires no intelligence or analysis — just raw computational power.

```
Try: "a", "b", "c", ... "z", "aa", "ab", ... "zz", "aaa", ...
Until: hash(candidate) == target_hash
```

---

## How Brute Force Works

```
┌─────────────────────────────────────┐
│  Attacker knows: target hash         │
│  Attacker has:   password database   │
└─────────────────────────────────────┘
                    ↓
    Try "a"     → H("a")     ≠ target
    Try "b"     → H("b")     ≠ target
    Try "c"     → H("c")     ≠ target
    ...
    Try "hunter2" → H("hunter2") = target ✓ FOUND!
```

---

## Search Space (Keyspace)

```
Characters × Length → Total combinations

Lowercase only:     26^L
Lowercase + upper:  52^L
Alphanumeric:       62^L
Full ASCII print:   95^L

L = password length
```

| Length | Lowercase | Alphanumeric | Full ASCII |
|--------|-----------|--------------|------------|
| 4 | 456,976 | 14,776,336 | 81,450,625 |
| 6 | 308,915,776 | 56,800,235,584 | ~7.3 billion |
| 8 | ~208 billion | ~218 trillion | ~6.6 quadrillion |
| 10 | ~141 trillion | ~839 quadrillion | ~59 quintillion |
| 12 | ~95 quadrillion | ~3.2 × 10^21 | ~5.4 × 10^23 |

---

## Attack Speed (Modern Hardware)

### MD5 (Unsalted)
```
CPU:  ~500 million/sec
GPU:  ~50 billion/sec (Nvidia RTX 4090)
```

### SHA-256 (Unsalted)
```
CPU:  ~40 million/sec
GPU:  ~8 billion/sec
```

### bcrypt (cost=12)
```
CPU:  ~2,000/sec
GPU:  ~12,000/sec (bcrypt resists GPU parallelism!)
```

### Argon2id (64MB, 3 iterations)
```
CPU:  ~300/sec
GPU:  ~300/sec (memory-hard — GPU provides no advantage!)
```

---

## Time to Brute Force

### Unsalted MD5 (GPU: 50B/sec)
| Password | Charset | Combinations | Time |
|----------|---------|--------------|------|
| 6 chars | lowercase | 308 million | 0.006 sec |
| 8 chars | lowercase | 208 billion | 4 sec |
| 8 chars | alphanum | 218 trillion | 1 hour |
| 10 chars | alphanum | 839 quad. | 193 days |
| 12 chars | full ASCII | 5.4 × 10^23 | millions of years |

### bcrypt cost=12 (GPU: 12K/sec)
| Password | Charset | Combinations | Time |
|----------|---------|--------------|------|
| 6 chars | lowercase | 308 million | 7 hours |
| 8 chars | lowercase | 208 billion | 550 years |
| 8 chars | alphanum | 218 trillion | 580,000 years |

**Conclusion: A strong KDF makes brute force infeasible!**

---

## Implementation Examples

### Python: Simple Brute Force
```python
import hashlib
import itertools
import string

def brute_force_md5(target_hash: str, max_length: int = 5) -> str | None:
    charset = string.ascii_lowercase + string.digits
    
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            candidate = ''.join(combo)
            h = hashlib.md5(candidate.encode()).hexdigest()
            if h == target_hash:
                return candidate
    return None

# Example (don't use MD5 for passwords!)
target = hashlib.md5(b"abc").hexdigest()
result = brute_force_md5(target, max_length=3)
print(f"Found: {result}")  # "abc"
```

### Python: Brute Force with Multiprocessing
```python
import hashlib
import itertools
import string
from multiprocessing import Pool

TARGET = hashlib.sha256(b"pass").hexdigest()
CHARSET = string.ascii_lowercase

def try_combination(args):
    combo, target = args
    candidate = ''.join(combo)
    if hashlib.sha256(candidate.encode()).hexdigest() == target:
        return candidate
    return None

def parallel_brute_force(length: int, workers: int = 4):
    with Pool(workers) as pool:
        combos = ((combo, TARGET) for combo in itertools.product(CHARSET, repeat=length))
        for result in pool.imap_unordered(try_combination, combos, chunksize=10000):
            if result:
                pool.terminate()
                return result
    return None
```

### Using Hashcat (Real Tool)
```bash
# Brute force all 1-8 lowercase chars against MD5 hash
hashcat -m 0 -a 3 hash.txt ?l?l?l?l?l?l?l?l

# Brute force all 6-char alphanumeric
hashcat -m 0 -a 3 hash.txt -i --pw-min=1 --pw-max=6 ?a?a?a?a?a?a

# Brute force bcrypt (much slower)
hashcat -m 3200 -a 3 bcrypt_hash.txt ?l?l?l?l?l?l

# Masks:
# ?l = lowercase (a-z)
# ?u = uppercase (A-Z)
# ?d = digits (0-9)
# ?s = special chars
# ?a = all printable ASCII
```

---

## Online vs Offline Brute Force

### Online Attack (Against a Login Form)
```
- Network limited: ~10 requests/sec
- Server can throttle/lockout after N failures
- CAPTCHA can stop automated attempts
- Much slower and detectable
```

### Offline Attack (Against Stolen Hash)
```
- Hardware limited: billions/sec possible
- No lockout mechanism — unlimited tries
- Attacker needs a copy of the hash
- The real threat model for password databases
```

---

## Defenses Against Brute Force

### Server-Side (Online)
```
✅ Rate limiting (max 5 attempts/minute)
✅ Account lockout after N failures
✅ Progressive delays (exponential backoff)
✅ CAPTCHA after failed attempts
✅ IP-based blocking
✅ Multi-factor authentication (MFA)
✅ Alert on suspicious login patterns
```

### Hash-Side (Offline)
```python
# Use slow hash functions
import bcrypt
from argon2 import PasswordHasher

# bcrypt: ~400ms per hash
bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))

# Argon2id: ~300ms per hash
ph = PasswordHasher(time_cost=3, memory_cost=65536)
ph.hash(password)

# Even with 1 billion attempts/sec on MD5,
# bcrypt/Argon2 reduce this to ~3,000/sec
```

### Password Policy
```
✅ Minimum 12 characters
✅ Encourage passphrases over complex short passwords
✅ Block known breached passwords (haveibeenpwned API)
✅ Don't limit character types unnecessarily
```

---

## Estimating Time to Crack (Formula)

```
T = C / R

T = time to crack (seconds)
C = total candidates = charset_size ^ password_length
R = hash rate (hashes per second)

Average time = T / 2 (on average, found halfway through)
```

```python
def time_to_crack(password_length: int, charset_size: int, hash_rate: int) -> float:
    """Returns average time in seconds to crack a password"""
    total = charset_size ** password_length
    return total / (2 * hash_rate)

# 8-char lowercase, bcrypt at 12k/sec
t = time_to_crack(8, 26, 12000)
print(f"Average time: {t/3600/24/365:.1f} years")  # ~275 years
```

---

## Best Practices
- **Always** use bcrypt, scrypt, or Argon2 for password storage
- Implement **rate limiting** on all authentication endpoints
- Use **MFA** to make brute force useless even if hash is cracked
- Enforce minimum **12-character passwords**
- Monitor and alert on **brute force patterns**
- Consider **HaveIBeenPwned** integration to block known breached passwords
