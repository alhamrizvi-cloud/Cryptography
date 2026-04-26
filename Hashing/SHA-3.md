
---

## 1. What SHA-3 Is

SHA-3 is a **modern cryptographic hash function** selected as a new standard to complement SHA-2.

It is based on a completely different design called:

> **Sponge Construction**

Common variants:

* **SHA3-256** → 256-bit output
* **SHA3-512** → 512-bit output

Example:

```text id="sha3ex"
Input  → hello  
SHA3-256 → 3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392
```

---

## 2. Why SHA-3 Exists

SHA-2 is still secure, but:

* It uses older structure (Merkle–Damgård)
* It has theoretical weaknesses (like length extension)

So SHA-3 was designed to:

* use a completely different internal design
* avoid structural weaknesses
* act as a backup standard if SHA-2 is ever broken

---

## 3. Core Properties

* One-way function
* Deterministic
* Fixed output length
* Strong avalanche effect
* No known practical attacks
* **Not vulnerable to length extension**

---

## 4. SHA-3 vs SHA-2

| Feature          | SHA-2              | SHA-3                           |
| ---------------- | ------------------ | ------------------------------- |
| Structure        | Merkle–Damgård     | Sponge                          |
| Length extension | Yes                | No                              |
| Security         | Strong             | Strong                          |
| Design           | Traditional        | Modern                          |
| Speed            | Faster in software | Competitive / hardware-friendly |

---

## 5. How SHA-3 Works (Simple Idea)

Instead of block chaining, SHA-3 uses a **sponge model**.

---

## 🧽 Sponge Construction

Two main phases:

### 1. Absorb phase

* Input is “absorbed” into internal state
* Mixed using permutations

---

### 2. Squeeze phase

* Output is “squeezed” from internal state
* Can produce variable-length output

---

### Internal state

* Large internal state (1600 bits)
* Split into:

  * **rate (r)** → input/output portion
  * **capacity (c)** → security portion

---

## 6. Why SHA-3 is Strong

* Completely different design than SHA-1 / SHA-2
* Resistant to known structural attacks
* No length extension vulnerability
* Flexible output sizes

---

## 7. Practical Usage

SHA-3 is used in:

* modern cryptographic systems
* blockchain (some variants)
* digital signatures
* secure hashing in new designs

Still less common than SHA-2, but growing.

---

## 8. Tools and Commands

### Linux

```bash id="sha3cmd"
echo -n "hello" | sha3sum 256
```

---

### Python

```python id="sha3py"
import hashlib

print(hashlib.sha3_256("hello".encode()).hexdigest())
```

---

## 9. Can SHA-3 be broken?

### Short answer:

No (currently)

---

### Only weak points:

* small input space
* poor implementation
* misuse in protocols

---

## 10. CTF Mindset

When you see SHA-3:

### Do NOT:

* attempt brute force blindly
* expect collisions or structural weaknesses

---

### Instead check:

* input size (small?)
* encoding tricks
* logic flaws
* how it’s used in system

---

## 11. Important Advantage Over SHA-2

### No Length Extension Attack

Unlike SHA-2:

```text id="sha3safe"
SHA3(secret || message)
```

cannot be extended into:

```text id="sha3fail"
SHA3(secret || message || extra)
```

So it is safer in naive constructions.

---

## 12. Variants (Important)

| Variant  | Output  |
| -------- | ------- |
| SHA3-224 | 224-bit |
| SHA3-256 | 256-bit |
| SHA3-384 | 384-bit |
| SHA3-512 | 512-bit |

## 13. Final Summary

SHA-3 is:

* Modern, secure hash function
* Based on sponge construction
* Resistant to structural weaknesses
* Not vulnerable to length extension
* Designed as future-proof alternative



