

## 1. What RIPEMD-160 Is

RIPEMD-160 is a **cryptographic hash function** designed as an alternative to SHA-1.

* Output size: **160 bits**
* Displayed as: **40 hexadecimal characters**

Example:

```text
Input  → hello  
RIPEMD-160 → 108f07b8382412612c048d07d13f814118445acd
```

---

## 2. Why It Exists

It was created to provide:

* a non-US alternative to SHA-1
* stronger design than older hashes like MD5

It improves security by using a more complex internal structure.

---

## 3. Core Properties

* One-way (cannot reverse hash → input)
* Deterministic
* Fixed output size (40 hex chars)
* Strong avalanche effect
* No practical full collision attacks known

---

## 4. How It Works (Simple Understanding)

RIPEMD-160 processes data in a unique way:

### Key idea:

It uses **two parallel computation paths**

```text
Left branch  → processes input
Right branch → processes input differently
```

Both branches:

* run multiple rounds
* use different constants and operations
* are merged at the end

---

### High-level steps:

1. Pad input
2. Split into 512-bit blocks
3. Process through 80 rounds
4. Combine parallel results
5. Output 160-bit hash

---

## 5. Where It Is Used (Important)

### Blockchain (especially Bitcoin)

Bitcoin uses:

```text
RIPEMD160(SHA256(public_key))
```

This is called:

## 👉 Hash160

---

### Why both SHA-256 and RIPEMD-160?

* SHA-256 → strong hashing
* RIPEMD-160 → shorter output (better for addresses)

This combination improves:

* usability
* compactness

---

## 6. Tools and Commands

### Linux

```bash
echo -n "hello" | openssl dgst -ripemd160
```

---

### Python

```python
import hashlib

h = hashlib.new('ripemd160')
h.update(b'hello')
print(h.hexdigest())
```

---

## 7. Security Status

RIPEMD-160 is:

* Still considered secure
* No practical full collisions known
* Less studied than SHA-2

---

### Limitations

* Smaller output than modern hashes
* Older design
* Not widely used outside blockchain

---

## 8. Comparison

| Feature  | RIPEMD-160 | SHA-256     |
| -------- | ---------- | ----------- |
| Output   | 160-bit    | 256-bit     |
| Security | Good       | Stronger    |
| Usage    | Blockchain | Everywhere  |
| Design   | Dual-path  | Single-path |

---

## 9. CTF Mindset

When you see RIPEMD-160:

* Do not try to reverse it directly
* Look for:

  * small input space
  * known values
  * chained hashes (e.g., SHA256 → RIPEMD160)

---

## 10. Key Insight

RIPEMD-160 is not popular because it’s the best.

It is used mainly because:

> systems like Bitcoin were built around it and kept it for compatibility

---

## 11. Final Summary

RIPEMD-160 is:

* A 160-bit cryptographic hash
* Designed as an alternative to SHA-1
* Still used in blockchain (Hash160)
* Secure but not modern standard

---

### Core Idea

RIPEMD-160 shows how:

> older but secure designs can remain important due to real-world adoption, especially in blockchain systems.
