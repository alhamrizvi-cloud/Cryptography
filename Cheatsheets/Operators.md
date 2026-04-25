
# 📘 Cryptography Core Operators Cheat Sheet

---

# 🔢 1. Arithmetic Operations

| Operation        | Meaning        | Math Form   | Python         |
| ---------------- | -------------- | ----------- | -------------- |
| Addition         | Add numbers    | `a + b`     | `a + b`        |
| Subtraction      | Difference     | `a - b`     | `a - b`        |
| Multiplication   | Product        | `a · b`     | `a * b`        |
| Division         | Real division  | `a / b`     | `a / b`        |
| Integer Division | Floor division | `⌊a / b⌋`   | `a // b`       |
| Modulus          | Remainder      | `a mod b`   | `a % b`        |
| Power            | Exponentiation | `a^b`       | `a ** b`       |
| Modular Power    | Power mod n    | `a^b mod n` | `pow(a, b, n)` |

---

# 🔐 2. Modular Arithmetic (CRYPTO CORE)

| Operation              | Meaning        | Math Form       | Python                       |
| ---------------------- | -------------- | --------------- | ---------------------------- |
| Modular Addition       | Add mod n      | `(a + b) mod n` | `(a + b) % n`                |
| Modular Subtraction    | Sub mod n      | `(a - b) mod n` | `(a - b) % n`                |
| Modular Multiplication | Multiply mod n | `(a · b) mod n` | `(a * b) % n`                |
| Modular Inverse        | Inverse of a   | `a⁻¹ mod n`     | `mod_inverse(a, n)`          |
| Modular Division       | Divide mod n   | `a · b⁻¹ mod n` | `(a * mod_inverse(b,n)) % n` |

---

# 🧮 3. Number Theory Operations

| Operation     | Meaning                 | Math Form            | Python             |
| ------------- | ----------------------- | -------------------- | ------------------ |
| GCD           | Greatest common divisor | `gcd(a, b)`          | `math.gcd(a, b)`   |
| Extended GCD  | Solve ax+by=1           | `ax + by = gcd(a,b)` | `sympy.gcdex(a,b)` |
| LCM           | Least common multiple   | `lcm(a, b)`          | `math.lcm(a, b)`   |
| Euler Totient | Count coprimes          | `φ(n)`               | custom / sympy     |
| Prime Check   | Is prime                | —                    | `sympy.isprime(a)` |
| Factorization | Break into primes       | `n = p·q`            | `factorint(n)`     |

---

# 🔁 4. RSA-Specific Operations

| Operation    | Meaning          | Math Form         | Python                |
| ------------ | ---------------- | ----------------- | --------------------- |
| Key Equation | RSA relation     | `ed ≡ 1 mod φ(n)` | `mod_inverse(e, phi)` |
| Encryption   | Encrypt message  | `C = M^e mod n`   | `pow(M, e, n)`        |
| Decryption   | Decrypt message  | `M = C^d mod n`   | `pow(C, d, n)`        |
| CRT Combine  | Combine residues | `x ≡ ai mod ni`   | `crt(n_list, a_list)` |

---

# 🔗 5. Bitwise Operations (IMPORTANT FOR ORACLES)

| Operation   | Meaning       | Math Form        | Python   |    |
| ----------- | ------------- | ---------------- | -------- | -- |
| AND         | Bitwise AND   | —                | `a & b`  |    |
| OR          | Bitwise OR    | —                | `a       | b` |
| XOR         | Exclusive OR  | —                | `a ^ b`  |    |
| NOT         | Bitwise NOT   | —                | `~a`     |    |
| Left Shift  | Multiply by 2 | `a << b = a·2^b` | `a << b` |    |
| Right Shift | Divide by 2   | `a >> b = a/2^b` | `a >> b` |    |

---

# 🔍 6. Comparison Operations

| Operation    | Meaning    | Math Form | Python   |
| ------------ | ---------- | --------- | -------- |
| Equal        | Equality   | `a = b`   | `a == b` |
| Not Equal    | Inequality | `a ≠ b`   | `a != b` |
| Less Than    | Comparison | `a < b`   | `a < b`  |
| Greater Than | Comparison | `a > b`   | `a > b`  |

---

# 🧠 7. Important Crypto Identities

| Concept                 | Math                |
| ----------------------- | ------------------- |
| RSA correctness         | `M^ed ≡ M mod n`    |
| Multiplicative property | `E(a)·E(b)=E(ab)`   |
| Fermat theorem          | `a^(p-1) ≡ 1 mod p` |
| Euler theorem           | `a^φ(n) ≡ 1 mod n`  |

---

# 🧩 8. Special Crypto Operations

| Operation       | Meaning           | Math          | Python                       |
| --------------- | ----------------- | ------------- | ---------------------------- |
| Bézout Identity | Combine exponents | `ax + by = 1` | `gcdex(a,b)`                 |
| CRT Solve       | Multi congruence  | system solve  | `crt()`                      |
| Integer Root    | nth root          | `√[b]{a}`     | `sympy.integer_nthroot(a,b)` |

---

# ⚡ 9. Quick Python Imports

```python id="gjqp7b"
import math
from sympy import mod_inverse, factorint, gcdex, isprime
from sympy.ntheory.modular import crt
```

---

# 🧠 10. Mental Mapping (VERY IMPORTANT)

| You See       | Use                |
| ------------- | ------------------ |
| `%`           | modular arithmetic |
| `pow(a,b,n)`  | fast RSA           |
| `gcd`         | factor leaks       |
| `mod_inverse` | find `d`           |
| `crt`         | combine values     |
| `gcdex`       | common modulus     |

