# scrypt

## What is scrypt?
scrypt is a **memory-hard password-based key derivation function** (KDF) created by Colin Percival in 2009. It was designed to make brute-force attacks expensive in both **time AND memory**, unlike bcrypt which is only CPU-expensive.

---

## Why scrypt?
- **Memory-hard**: requires large amounts of RAM, making GPU/ASIC attacks costly
- Configurable CPU, memory, and parallelization parameters
- Used in cryptocurrencies (Litecoin, Dogecoin)
- NIST-recommended KDF

---

## How scrypt Works

```
password + salt + (N, r, p) → derived key
```

### Parameters
| Parameter | Meaning | Typical Value |
|-----------|---------|---------------|
| `N` | CPU/memory cost (must be power of 2) | 16384, 65536 |
| `r` | Block size (affects memory) | 8 |
| `p` | Parallelization factor | 1 |
| `dkLen` | Output key length (bytes) | 32, 64 |

### Memory Usage Formula
```
Memory = 128 × N × r bytes
Example: N=16384, r=8 → 128 × 16384 × 8 = 16 MB
```

---

## Algorithm Steps
1. **PBKDF2** with HMAC-SHA256 to generate initial blocks
2. **ROMix** — fills a large memory buffer with pseudo-random data, then reads it in a random order (memory-hard step)
3. **BlockMix** with Salsa20/8 core — mixes 64-byte blocks
4. Final **PBKDF2** to produce the derived key

---

## Implementation Examples

### Python
```python
import hashlib, os

password = b"mysecretpassword"
salt = os.urandom(16)

# N=16384, r=8, p=1, dklen=32
key = hashlib.scrypt(password, salt=salt, n=16384, r=8, p=1, dklen=32)
print(key.hex())
```

### Node.js
```javascript
const crypto = require('crypto');

const password = Buffer.from('mysecretpassword');
const salt = crypto.randomBytes(16);

crypto.scrypt(password, salt, 32, { N: 16384, r: 8, p: 1 }, (err, key) => {
    console.log(key.toString('hex'));
});
```

### Go
```go
import "golang.org/x/crypto/scrypt"

key, err := scrypt.Key([]byte("password"), salt, 16384, 8, 1, 32)
```

### Rust
```rust
use scrypt::{scrypt, Params};

let params = Params::new(14, 8, 1, 32).unwrap(); // N=2^14
scrypt(password, salt, &params, &mut output).unwrap();
```

---

## Parameter Tuning Guide

| Use Case | N | r | p | Memory |
|----------|---|---|---|--------|
| Interactive login | 16384 | 8 | 1 | 16 MB |
| File encryption | 65536 | 8 | 1 | 64 MB |
| High security | 262144 | 8 | 1 | 256 MB |
| Low memory device | 8192 | 8 | 1 | 8 MB |

---

## scrypt vs Other KDFs

| Feature | PBKDF2 | bcrypt | scrypt | Argon2 |
|---------|--------|--------|--------|--------|
| Memory-hard | ❌ | ❌ | ✅ | ✅ |
| CPU-hard | ✅ | ✅ | ✅ | ✅ |
| Parallelism control | ✅ | ❌ | ✅ | ✅ |
| GPU resistance | Low | Medium | High | Highest |
| Side-channel safe | ❌ | ❌ | ❌ | ✅ (id) |

---

## Attacks Against scrypt

| Attack | Effectiveness |
|--------|--------------|
| Brute Force | Very expensive (time + memory) |
| GPU Attack | Limited by memory requirement |
| ASIC Attack | Costly but possible with enough RAM |
| Time-memory tradeoff | Possible if N is too low |

---

## Real-World Usage
- **Litecoin** — uses scrypt as its proof-of-work algorithm
- **Dogecoin** — same as Litecoin
- **macOS** — used in FileVault disk encryption key derivation
- **WiFi WPA3** — SAE uses scrypt-like memory hardness

---

## Best Practices
- Use `N ≥ 16384` (higher is better if RAM allows)
- Always store the **salt alongside the hash**
- Benchmark on your hardware: target **100–300ms** for login
- Prefer **Argon2id** for new systems (more modern and flexible)
