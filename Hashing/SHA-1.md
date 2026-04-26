
## 1. What SHA-1 Is

SHA-1 is a **cryptographic hash function** designed to produce a fixed-size output from any input.

* Output size: **160 bits**
* Displayed as: **40 hexadecimal characters**

Example:

```text id="sha1ex"
Input  → hello  
SHA-1  → aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
```

## 2. Core Properties

* One-way function (not reversible)
* Deterministic (same input → same output)
* Fixed-length output (40 hex chars)
* Avalanche effect (small change → huge difference)

## 3. SHA-1 vs MD5 (Quick Comparison)

| Feature     | MD5        | SHA-1      |
| ----------- | ---------- | ---------- |
| Output size | 128-bit    | 160-bit    |
| Length      | 32 hex     | 40 hex     |
| Security    | Broken     | Broken     |
| Speed       | Very fast  | Fast       |
| Usage today | Deprecated | Deprecated |

SHA-1 was designed to improve MD5, but it is now also broken.

## 4. How SHA-1 Works (Simple Structure)

SHA-1 follows a **Merkle–Damgård construction**.

### Step 1: Padding

Input is padded to fit 512-bit blocks.

### Step 2: Split into blocks

Data is divided into 512-bit chunks.

### Step 3: Initialize variables

```text id="sha1buf"
A, B, C, D, E
```

(5 internal 32-bit registers)

### Step 4: Compression rounds

Each block goes through **80 rounds** of:

* bitwise operations
* rotations
* modular addition

---

### Step 5: Output

Final values of A, B, C, D, E are combined:

```text id="sha1out"
→ 160-bit hash
```

## 5. Why SHA-1 Cannot Be Reversed

Same reason as MD5:

* Infinite input space
* Fixed output size

So:

```text id="sha1rev1"
hash → original input ❌ not possible
```

Only way to recover input is:

* guessing
* brute force
* dictionary attacks


## 6. Practical Usage (Old + Legacy)

SHA-1 was used in:

* SSL/TLS certificates (old)
* Git commit hashing (historically)
* File verification
* Digital signatures

Now mostly deprecated.

## 7. Tools and Commands

### Generate SHA-1

#### Linux

```bash id="sha1cmd"
echo -n "hello" | sha1sum
``
#### Python

```python id="sha1py"
import hashlib

print(hashlib.sha1("hello".encode()).hexdigest())
```

---

## 8. “Cracking” SHA-1

Same concept as MD5:

### 1. Online lookup

Works for common values.

### 2. John the Ripper

```bash id="sha1john"
john --format=raw-sha1 hash.txt --wordlist=rockyou.txt
```

### 3. Hashcat

```bash id="sha1hashcat"
hashcat -m 100 hash.txt rockyou.txt
```
### 4. Brute force (Python)

```python id="sha1bf"
import hashlib

target = "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d"

for i in range(1000000):
    guess = str(i)
    if hashlib.sha1(guess.encode()).hexdigest() == target:
        print("Found:", guess)
        break
```

## 9. Why SHA-1 is Broken

### 1. Collision attacks

Two different inputs can produce same hash:

```text id="sha1col"
m1 ≠ m2  
SHA1(m1) = SHA1(m2)
```

### 2. Real-world attack

The **SHAttered attack (2017)** proved practical collisions.

Impact:

* fake files with same hash possible
* digital signatures can be forged

---

### 3. Still fast

Not ideal for password hashing:

* brute force still feasible

---

## 10. Special Weakness — Length Extension Attack

Because SHA-1 uses Merkle–Damgård:

If you know:

```text id="sha1le"
SHA1(secret || message)
```

You can compute:

```text id="sha1le2"
SHA1(secret || message || extra)
```

WITHOUT knowing the secret.

---

### Why this matters

Breaks systems using:

```text id="bad"
hash = SHA1(secret + data)
```

---

## 11. CTF Mindset

When you see SHA-1:

### Step 1:

Identify (40 hex chars)

### Step 2:

Check if:

* simple hash → brute force
* salted → harder
* part of protocol → look for logic flaws

### Step 3:

Look for:

* length extension vulnerability
* weak password
* predictable input

---

## 12. Real-World Status

SHA-1 is:

* Cryptographically broken
* Deprecated in modern security
* Still appears in:

  * legacy systems
  * CTF challenges

---

## 13. Final Summary

SHA-1 is:

* Stronger than MD5 (historically)
* Now broken due to collisions
* Still one-way (not reversible)
* Vulnerable to structural attacks

---

### Core idea:

SHA-1 is not secure for modern cryptography,
but still widely used in CTFs for attack practice.
