# Pepper

## What is a Pepper?
A **pepper** is a secret value added to a password before hashing — similar to a salt, but with one critical difference: **the pepper is NOT stored in the database**. It is kept secret, typically in application configuration or a secrets manager.

```
hash = H(password + salt + pepper)
```

---

## Salt vs Pepper Comparison

| Property | Salt | Pepper |
|----------|------|--------|
| Stored in DB | ✅ Yes (plaintext) | ❌ No |
| Secret | ❌ No | ✅ Yes |
| Unique per user | ✅ Yes | ❌ No (shared) |
| Purpose | Prevent rainbow tables | Protect if DB is leaked |
| Rotation | Per password change | Difficult (requires rehash all) |

---

## Why Use a Pepper?

### Scenario: Database Breach
```
Attacker steals the database:
├── Without pepper: has salt + hash → can attempt cracking
└── With pepper:    has salt + hash → CANNOT crack without pepper value
                                      (pepper is not in the DB)
```

Even if an attacker dumps your entire database, they **cannot crack the hashes** without the pepper — because they're missing a crucial input to the hash function.

---

## How Peppers Work

```
┌──────────────┐
│   Password   │
│  "hunter2"   │──┐
└──────────────┘  │
                  ├──▶ H(password + salt + pepper) ──▶ stored_hash
┌──────────────┐  │
│     Salt     │──┘
│  (in DB)     │  
└──────────────┘  
                  
┌──────────────┐  (not in DB — stored in secrets manager / env var)
│    Pepper    │
│  "X9kP2mL8" │
└──────────────┘
```

---

## Implementation Examples

### Python
```python
import bcrypt
import os

PEPPER = os.environ.get("PASSWORD_PEPPER")  # From environment variable

def hash_password(password: str) -> bytes:
    peppered = (password + PEPPER).encode()
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(peppered, salt)

def verify_password(password: str, stored_hash: bytes) -> bool:
    peppered = (password + PEPPER).encode()
    return bcrypt.checkpw(peppered, stored_hash)
```

### Node.js
```javascript
const bcrypt = require('bcrypt');
const PEPPER = process.env.PASSWORD_PEPPER;

async function hashPassword(password) {
    const peppered = password + PEPPER;
    return await bcrypt.hash(peppered, 12);
}

async function verifyPassword(password, storedHash) {
    const peppered = password + PEPPER;
    return await bcrypt.compare(peppered, storedHash);
}
```

### Using HMAC as Pepper (More Secure Approach)
```python
import hmac
import hashlib
import bcrypt
import os

PEPPER_KEY = os.environ.get("PEPPER_KEY")  # Secret key

def apply_pepper(password: str) -> bytes:
    # Use HMAC-SHA256 with pepper as the key
    return hmac.new(
        PEPPER_KEY.encode(),
        password.encode(),
        hashlib.sha256
    ).digest()

def hash_password(password: str) -> bytes:
    peppered = apply_pepper(password)
    return bcrypt.hashpw(peppered, bcrypt.gensalt(12))

def verify_password(password: str, stored_hash: bytes) -> bool:
    peppered = apply_pepper(password)
    return bcrypt.checkpw(peppered, stored_hash)
```

---

## Pepper Storage Locations

| Location | Security | Complexity |
|----------|----------|------------|
| Environment variable | Medium | Low |
| `.env` file (not in repo) | Medium | Low |
| Secrets manager (AWS, Vault) | High | Medium |
| HSM (Hardware Security Module) | Highest | High |
| Config file (never in source control) | Low-Medium | Low |

---

## Pepper Rotation Problem

Rotating a pepper is **difficult** because all existing hashes need to be rehashed:

```python
# Rotation strategy: versioned peppers
PEPPERS = {
    "v1": "old_pepper_value",
    "v2": "new_pepper_value",  # current
}

def verify_with_rotation(password, stored_hash, pepper_version):
    pepper = PEPPERS[pepper_version]
    peppered = (password + pepper).encode()
    return bcrypt.checkpw(peppered, stored_hash)

# On successful login with old version: rehash with new pepper
```

---

## Attacks Defeated by Pepper

| Attack | Defeated? |
|--------|-----------|
| Database dump + offline cracking | ✅ Yes (no pepper = can't crack) |
| Rainbow Tables | ✅ Yes (combined with salt) |
| SQL Injection hash theft | ✅ Yes |
| Brute force with known pepper | ❌ No |
| Insider threat (attacker has DB + source) | ❌ No |

---

## Common Mistakes

### ❌ Storing pepper in database
```sql
-- WRONG: pepper in DB defeats its purpose
ALTER TABLE users ADD COLUMN pepper VARCHAR(32);
```

### ❌ Same pepper as salt
```python
# WRONG: pepper should be application-wide secret, not per-user
pepper = salt  
```

### ❌ Hardcoding in source code
```python
PEPPER = "my_secret_pepper"  # WRONG: if source leaks, pepper leaks
```

### ✅ Correct: Environment / Secrets Manager
```python
PEPPER = os.environ["PASSWORD_PEPPER"]  # Never commit this value
```

---

## Best Practices
- Store pepper in **environment variables** or a **secrets manager** (never in DB or source)
- Use **HMAC** with the pepper as a key rather than simple concatenation
- Implement **versioned peppers** to allow future rotation
- Combine with proper **salting** and a strong KDF (bcrypt/Argon2)
- Minimum pepper length: **32 random bytes** (256 bits)
- Document your pepper rotation strategy before you need it
