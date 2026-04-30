# Length Extension Attack

## What is a Length Extension Attack?
A **length extension attack** exploits the Merkle-Damgård construction used in MD5, SHA-1, and SHA-2. If an attacker knows `H(secret || message)` and the length of `secret`, they can compute `H(secret || message || padding || extension)` **without knowing the secret**.

```
Known:    H(secret || message) and len(secret)
Compute:  H(secret || message || padding || attacker_data)
Without:  knowing `secret`!
```

---

## Why It Happens: Merkle-Damgård Construction

```
SHA-256 processes data in 64-byte blocks:

[IV] → compress(block1) → compress(block2) → [final state] → hash

The "final state" IS the hash output.
If attacker has the hash, they have the internal state!
They can resume hashing from that state → append more data.
```

---

## Step-by-Step Attack

```
Scenario: API uses H(secret || params) as authentication token

Server computes:
  H("s3cr3t" || "user=alice&amount=100") = abc123...

Attacker knows:
  - The hash: abc123...
  - The message: "user=alice&amount=100"
  - The secret length (guessable or known): 6

Attacker can compute:
  H("s3cr3t" || "user=alice&amount=100" || PADDING || "&admin=true")
  = def456...

Without knowing "s3cr3t"!

Server verifies def456... → matches → attacker is authenticated!
```

---

## The Padding Structure

SHA-256 padding added after the original message:
```
[message] [0x80] [0x00 * n] [64-bit length]

Example for "user=alice&amount=100" with 6-byte secret:
Total input: 6 + 22 = 28 bytes
Padding: 0x80 then zeros until 56 bytes, then 8-byte length
= 0x80 0x00*27 0x000000000000e0 (224 bits = 28 bytes)
```

---

## Practical Attack with Python

```python
import struct
import hashlib

def sha256_padding(msg_len: int) -> bytes:
    """Compute SHA-256 padding for a message of msg_len bytes"""
    padding = b'\x80'
    padding += b'\x00' * ((55 - msg_len) % 64)
    padding += struct.pack('>Q', msg_len * 8)  # 64-bit big-endian bit length
    return padding

def length_extension_attack(
    known_hash: str,    # H(secret || message)
    secret_len: int,    # length of secret in bytes
    original_msg: bytes,
    extension: bytes
) -> tuple[bytes, str]:
    """
    Compute H(secret || original_msg || padding || extension)
    without knowing the secret.
    """
    # The padding that was added after (secret || original_msg)
    total_len = secret_len + len(original_msg)
    padding = sha256_padding(total_len)
    
    # Extract internal state from the known hash
    h = [int(known_hash[i:i+8], 16) for i in range(0, 64, 8)]
    
    # Resume SHA-256 from the known state with the extension
    # (simplified — real implementation resumes the compression function)
    forged_msg = original_msg + padding + extension
    
    # In practice, use a library like hash_extender or hlextend
    return forged_msg, "forged_hash_here"

# Real usage:
# pip install hlextend
import hlextend

sha = hlextend.new('sha256')
forged_msg, forged_hash = sha.extend(
    b'&admin=true',               # Extension
    b'user=alice&amount=100',     # Known message
    6,                            # Secret length
    'abc123...'                   # Known hash H(secret||message)
)
```

### Using hash_extender (CLI tool)
```bash
# Install
git clone https://github.com/iagox86/hash_extender
make

# Attack
./hash_extender \
  --data "user=alice&amount=100" \
  --secret 6 \
  --append "&admin=true" \
  --signature abc123... \
  --format sha256

# Output:
# New signature: def456...
# New string:    user=alice&amount=100\x80\x00...\x00&admin=true
```

---

## Vulnerable Pattern

```python
# ❌ VULNERABLE: H(secret || message)
import hashlib, os

SECRET = os.environ['API_SECRET']

def generate_token(message: str) -> str:
    return hashlib.sha256((SECRET + message).encode()).hexdigest()

def verify_token(message: str, token: str) -> bool:
    return generate_token(message) == token

# Attacker can forge tokens for extended messages!
```

---

## Secure Alternatives

### HMAC (Fix — Use This!) ✅
```python
import hmac, hashlib, os

SECRET = os.environ['API_SECRET'].encode()

def generate_token(message: str) -> str:
    return hmac.new(SECRET, message.encode(), hashlib.sha256).hexdigest()

def verify_token(message: str, token: str) -> bool:
    expected = generate_token(message)
    return hmac.compare_digest(expected, token)  # Constant-time comparison!

# HMAC is NOT vulnerable to length extension:
# HMAC(k, m) = H((k ⊕ opad) || H((k ⊕ ipad) || m))
# The outer hash prevents extension of the inner hash
```

### SHA-3 / BLAKE2 ✅
```python
import hashlib

# SHA-3 uses sponge construction — NOT vulnerable to length extension
token = hashlib.sha3_256((secret + message).encode()).hexdigest()

# BLAKE2 also not vulnerable
token = hashlib.blake2b((secret + message).encode()).hexdigest()
```

---

## Which Algorithms Are Vulnerable?

| Algorithm | Construction | Vulnerable? |
|-----------|-------------|-------------|
| MD5 | Merkle-Damgård | ✅ Yes |
| SHA-1 | Merkle-Damgård | ✅ Yes |
| SHA-256 | Merkle-Damgård | ✅ Yes |
| SHA-512 | Merkle-Damgård | ✅ Yes |
| SHA-3 | Sponge | ❌ No |
| BLAKE2 | HAIFA | ❌ No |
| BLAKE3 | Merkle tree | ❌ No |
| HMAC-* | Double hash | ❌ No |

---

## Best Practices
- **Always use HMAC** when authenticating messages with a secret key
- Never construct `H(secret || message)` — use `HMAC(secret, message)` instead
- Use **constant-time comparison** (`hmac.compare_digest`) to prevent timing attacks
- SHA-3 and BLAKE2/BLAKE3 are not vulnerable if you must use raw hashing
- Audit any API that uses hash-based authentication tokens
