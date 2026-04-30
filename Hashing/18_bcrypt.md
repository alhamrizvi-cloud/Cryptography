# bcrypt

## What is bcrypt?
bcrypt is a **password hashing function** designed by Niels Provos and David Mazières in 1999, based on the Blowfish cipher. It is specifically designed to be **slow and computationally expensive**, making brute-force attacks difficult.

---

## Why bcrypt?
- Built-in **salt** generation (prevents rainbow table attacks)
- **Adaptive cost factor** (work factor can be increased as hardware improves)
- Widely supported across languages and frameworks
- Time-tested and battle-hardened

---

## How bcrypt Works

```
password + salt → bcrypt(cost factor) → 60-char hash string
```

### Hash Format
```
$2b$12$SSSSSSSSSSSSSSSSSSSSSSHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
│   │  │                    │
│   │  └── Salt (22 chars)  └── Hash (31 chars)
│   └── Cost factor (work factor)
└── Version ($2a$, $2b$, $2y$)
```

### Example Output
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6y8T9G6hm6
```

---

## Cost Factor (Work Factor)

| Cost | Approx. Time (modern CPU) |
|------|--------------------------|
| 10   | ~100ms                   |
| 12   | ~400ms                   |
| 14   | ~1.5s                    |
| 16   | ~6s                      |

Higher cost = slower hashing = harder to crack.

---

## Implementation Examples

### Python
```python
import bcrypt

# Hashing
password = b"mysecretpassword"
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password, salt)
print(hashed)

# Verifying
if bcrypt.checkpw(password, hashed):
    print("Password matches!")
```

### Node.js
```javascript
const bcrypt = require('bcrypt');

// Hashing
const saltRounds = 12;
const hash = await bcrypt.hash('mysecretpassword', saltRounds);

// Verifying
const match = await bcrypt.compare('mysecretpassword', hash);
console.log(match); // true
```

### Go
```go
import "golang.org/x/crypto/bcrypt"

// Hashing
hash, err := bcrypt.GenerateFromPassword([]byte("password"), 12)

// Verifying
err = bcrypt.CompareHashAndPassword(hash, []byte("password"))
```

---

## Internals: EksBlowfish Algorithm
1. Takes password + salt + cost
2. Runs `2^cost` rounds of key setup
3. Encrypts the string `"OrpheanBeholderScryDoubt"` 64 times
4. Returns the resulting ciphertext as the hash

---

## Limitations
- Max password length: **72 bytes** (longer passwords are silently truncated)
- Not ideal for bulk data encryption (designed only for passwords)
- Slower than Argon2 in memory-hardness

---

## bcrypt vs Other Password Hashing Functions

| Feature         | bcrypt | scrypt | Argon2 |
|----------------|--------|--------|--------|
| Salt built-in   | ✅     | ✅     | ✅     |
| Memory-hard     | ❌     | ✅     | ✅     |
| GPU resistance  | Medium | High   | Highest|
| Year            | 1999   | 2009   | 2015   |
| PHC Winner      | ❌     | ❌     | ✅     |

---

## Attacks Against bcrypt
| Attack | Effectiveness |
|--------|--------------|
| Brute Force | Very slow due to cost factor |
| Rainbow Tables | Prevented by built-in salt |
| GPU Acceleration | Limited (bcrypt is GPU-unfriendly) |
| Password truncation exploit | Possible if passwords > 72 bytes |

---

## Best Practices
- Use cost factor **12+** for production
- Always use the **verify function** (never re-hash to compare)
- Update cost factor periodically as hardware improves
- Handle the **72-byte limit** by pre-hashing with SHA-256 if needed
