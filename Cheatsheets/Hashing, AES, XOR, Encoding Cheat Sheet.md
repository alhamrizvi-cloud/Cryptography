

# 📘 Cryptography Core — Hashing, AES, XOR, Encoding Cheat Sheet

---

# 🔐 1. HASHING OPERATIONS

| Operation        | Meaning                | Math Form   | Python                          |            |                 |      |                        |
| ---------------- | ---------------------- | ----------- | ------------------------------- | ---------- | --------------- | ---- | ---------------------- |
| Hash             | One-way function       | `h = H(m)`  | `hashlib.sha256(m).hexdigest()` |            |                 |      |                        |
| Verify Hash      | Check equality         | `H(m) = h`  | `hashlib.sha256(m)==h`          |            |                 |      |                        |
| Double Hash      | Hash twice             | `H(H(m))`   | `sha256(sha256(m))`             |            |                 |      |                        |
| Salted Hash      | Add randomness         | `H(m        |                                 | s)`        | `sha256(m + s)` |      |                        |
| Length Extension | Exploit Merkle-Damgård | `H(m        |                                 | x)`        | `hashpump` tool |      |                        |
| HMAC             | Keyed hash             | `H(k ⊕ opad |                                 | H(k ⊕ ipad |                 | m))` | `hmac.new(k,m,sha256)` |

---

## 🔹 Python Example

```python id="h1c2df"
import hashlib

m = b"hello"

h = hashlib.sha256(m).hexdigest()
print(h)
```

---

# 🔑 2. XOR OPERATIONS (VERY IMPORTANT)

| Operation      | Meaning       | Math Form                   | Python           |
| -------------- | ------------- | --------------------------- | ---------------- |
| XOR            | Bitwise XOR   | `c = a ⊕ b`                 | `a ^ b`          |
| Reverse XOR    | Recover value | `a = c ⊕ b`                 | `c ^ b`          |
| XOR Encryption | Simple cipher | `C = M ⊕ K`                 | `bytes([m ^ k])` |
| Repeating XOR  | Key repeats   | `C[i]=M[i]⊕K[i mod len(K)]` | loop             |
| XOR Property   | Self-inverse  | `a ⊕ b ⊕ b = a`             | same             |

---

## 🔹 Python Example

```python id="9h8b2f"
a = 10
b = 5

c = a ^ b
print(c)

# reverse
print(c ^ b)
```

---

# 🔒 3. AES (SYMMETRIC ENCRYPTION)

## Modes Overview

| Mode | Meaning            | Formula                       | Python         |
| ---- | ------------------ | ----------------------------- | -------------- |
| ECB  | Independent blocks | `Ci = AES(K, Mi)`             | `AES.MODE_ECB` |
| CBC  | Chained blocks     | `Ci = AES(K, Mi ⊕ Ci-1)`      | `AES.MODE_CBC` |
| CTR  | Stream cipher      | `Ci = Mi ⊕ AES(K, nonce+ctr)` | `AES.MODE_CTR` |
| GCM  | Authenticated      | encryption + tag              | `AES.MODE_GCM` |

---

## 🔹 Core AES Operations

| Operation | Meaning        | Math              | Python             |
| --------- | -------------- | ----------------- | ------------------ |
| Encrypt   | Encrypt block  | `C = AES(K, M)`   | `cipher.encrypt()` |
| Decrypt   | Decrypt block  | `M = AES⁻¹(K, C)` | `cipher.decrypt()` |
| Padding   | Add bytes      | PKCS#7            | `pad()`            |
| Unpadding | Remove padding | —                 | `unpad()`          |

---

## 🔹 Python Example (CBC)

```python id="i6l2c8"
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'1234567890123456'
cipher = AES.new(key, AES.MODE_CBC)

ct = cipher.encrypt(pad(b"hello", 16))
print(ct)
```

---

# ⚠️ AES Weakness Patterns

| Problem            | Result       |
| ------------------ | ------------ |
| ECB mode           | pattern leak |
| Reused IV (CBC)    | predictable  |
| Reused nonce (CTR) | key recovery |
| No authentication  | tampering    |

---

# 🔁 4. ENCODING OPERATIONS

| Encoding      | Meaning       | Math     | Python               |
| ------------- | ------------- | -------- | -------------------- |
| ASCII         | char → number | `ord(c)` | `ord('A')`           |
| Char          | number → char | —        | `chr(65)`            |
| Hex Encode    | bytes → hex   | —        | `.hex()`             |
| Hex Decode    | hex → bytes   | —        | `bytes.fromhex()`    |
| Base64 Encode | binary → text | —        | `base64.b64encode()` |
| Base64 Decode | text → binary | —        | `base64.b64decode()` |
| Binary        | base-2        | —        | `bin(a)`             |

---

## 🔹 Python Example

```python id="2k3d8s"
import base64

m = b"hello"

enc = base64.b64encode(m)
print(enc)

dec = base64.b64decode(enc)
print(dec)
```

---

# 🔗 5. COMMON CTF PATTERNS

| Pattern           | What It Means  | Action             |
| ----------------- | -------------- | ------------------ |
| Base64 string     | encoded data   | decode             |
| Hex string        | encoded bytes  | decode             |
| Repeating XOR     | weak cipher    | brute key          |
| ECB blocks repeat | AES ECB        | detect pattern     |
| Hash given        | verify / crack | brute / dictionary |
| Same keystream    | XOR reuse      | XOR ciphertexts    |

---

# 🧠 6. IMPORTANT IDENTITIES

| Concept        | Formula         |
| -------------- | --------------- |
| XOR cancel     | `a ⊕ b ⊕ b = a` |
| XOR same       | `a ⊕ a = 0`     |
| Hash one-way   | cannot invert   |
| AES reversible | needs key       |
| CTR mode       | stream cipher   |

---

# ⚡ 7. QUICK IMPORTS

```python id="d7kl3s"
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
```

---

# 🧠 8. MENTAL MODEL

| You See          | Think              |
| ---------------- | ------------------ |
| `==` hashes      | brute / dictionary |
| repeating blocks | ECB                |
| XOR patterns     | key reuse          |
| base64/hex       | decode first       |
| nonce reuse      | CTR break          |

---

# ✅ FINAL NOTE

This + RSA sheet = **complete CTF crypto toolkit**

```text
RSA → math attacks
AES/XOR → implementation attacks
Hash → integrity / brute
Encoding → preprocessing
```
