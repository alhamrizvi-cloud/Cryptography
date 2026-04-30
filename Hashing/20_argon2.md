# Argon2

## What is Argon2?
Argon2 is the **winner of the Password Hashing Competition (PHC) in 2015**. It is the current gold standard for password hashing and key derivation. Designed by Alex Biryukov, Daniel Dinu, and Dmitry Khovratovich.

---

## Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| **Argon2d** | Data-dependent memory access | Cryptocurrencies (GPU resistance) |
| **Argon2i** | Data-independent memory access | Password hashing (side-channel safe) |
| **Argon2id** | Hybrid of d and i ✅ RECOMMENDED | General purpose — best of both |

> **Always use Argon2id** unless you have a specific reason for the others.

---

## Parameters

| Parameter | Symbol | Meaning | Recommended |
|-----------|--------|---------|-------------|
| Memory cost | `m` | RAM usage in KiB | ≥ 64 MB (65536 KiB) |
| Time cost | `t` | Number of iterations | ≥ 3 |
| Parallelism | `p` | Number of threads | 4 |
| Hash length | `T` | Output size in bytes | 32 |
| Salt length | — | Random salt | 16 bytes |

---

## Hash Format (PHC String Format)
```
$argon2id$v=19$m=65536,t=3,p=4$<salt_base64>$<hash_base64>
```

Example:
```
$argon2id$v=19$m=65536,t=3,p=4$c29tZXNhbHQ$RdescudvJCsgt3ub+b+dWRWJTmaaJObG
```

---

## How Argon2 Works

### Step 1: Fill Memory Matrix
- Allocates `m` KiB of RAM divided into 1 KiB blocks
- Fills memory with pseudo-random data derived from password + salt

### Step 2: Mix Memory
- Makes `t` passes over the memory
- Each block depends on previous blocks (Argon2i: pseudo-random, Argon2d: data-dependent)

### Step 3: Finalize
- XOR the last column of blocks
- Apply Blake2b compression
- Output hash

---

## Implementation Examples

### Python
```python
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,       # iterations
    memory_cost=65536, # 64 MB in KiB
    parallelism=4,
    hash_len=32,
    salt_len=16
)

# Hash
hash = ph.hash("mysecretpassword")
print(hash)

# Verify
try:
    ph.verify(hash, "mysecretpassword")
    print("Valid!")
except:
    print("Invalid!")

# Check if rehash needed (parameters changed)
if ph.check_needs_rehash(hash):
    hash = ph.hash("mysecretpassword")
```

### Node.js
```javascript
const argon2 = require('argon2');

// Hash
const hash = await argon2.hash('mysecretpassword', {
    type: argon2.argon2id,
    memoryCost: 65536,  // 64 MB
    timeCost: 3,
    parallelism: 4,
});

// Verify
const valid = await argon2.verify(hash, 'mysecretpassword');
console.log(valid); // true
```

### Go
```go
import "github.com/alexedwards/argon2id"

// Hash with default params
hash, err := argon2id.CreateHash("password", argon2id.DefaultParams)

// Verify
match, err := argon2id.ComparePasswordAndHash("password", hash)
```

### Rust
```rust
use argon2::{Argon2, PasswordHash, PasswordHasher, PasswordVerifier};
use argon2::password_hash::{rand_core::OsRng, SaltString};

let salt = SaltString::generate(&mut OsRng);
let argon2 = Argon2::default();
let hash = argon2.hash_password(password.as_bytes(), &salt).unwrap();

// Verify
let parsed = PasswordHash::new(&hash_str).unwrap();
argon2.verify_password(password.as_bytes(), &parsed).is_ok()
```

### PHP
```php
// PHP 7.2+ has native Argon2 support
$hash = password_hash('mysecretpassword', PASSWORD_ARGON2ID, [
    'memory_cost' => 65536,
    'time_cost'   => 3,
    'threads'     => 4,
]);

$valid = password_verify('mysecretpassword', $hash);
```

---

## OWASP Recommended Parameters (2024)

| Profile | m (KiB) | t | p |
|---------|---------|---|---|
| Minimum | 19456 (19 MB) | 2 | 1 |
| Balanced | 65536 (64 MB) | 3 | 4 |
| High Security | 262144 (256 MB) | 3 | 4 |

---

## Argon2 vs Competitors

| Feature | PBKDF2 | bcrypt | scrypt | Argon2id |
|---------|--------|--------|--------|----------|
| Memory-hard | ❌ | ❌ | ✅ | ✅ |
| Side-channel safe | ❌ | ❌ | ❌ | ✅ |
| GPU resistance | Low | Medium | High | Highest |
| Parallelism | ✅ | ❌ | ✅ | ✅ |
| PHC Winner | ❌ | ❌ | ❌ | ✅ |
| RFC Standard | ✅ | ❌ | ❌ | RFC 9106 |

---

## Attacks Against Argon2

| Attack | Effectiveness |
|--------|--------------|
| Brute Force | Extremely expensive |
| GPU | Very limited (memory-hard) |
| ASIC | Economically infeasible at high `m` |
| Side-channel | Prevented by Argon2i/id |
| Time-memory tradeoff | Mitigated by high `t` |

---

## Best Practices
- **Always use Argon2id** for new applications
- Target **300–500ms** hash time for logins
- Use **minimum 16-byte random salt**
- Store the full PHC string (includes parameters + salt + hash)
- Implement **rehashing** when parameters are upgraded
