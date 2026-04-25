
# 📘 RSA Attacks Master Table

| Attack                            | When to Use                        | What It Is                            | Core Math                                                                    |
| --------------------------------- | ---------------------------------- | ------------------------------------- | ---------------------------------------------------------------------------- |
| **Factoring Attack**              | Small / weak `n`                   | Factor `n = p·q`, compute private key | `φ(n) = (p−1)(q−1)` → `d = e⁻¹ mod φ(n)`                                     |
| **Fermat Attack**                 | `p ≈ q` (close primes)             | Uses difference of squares            | `n = a² − b² = (a−b)(a+b)`                                                   |
| **Common Modulus Attack**         | Same `n`, different `e`, same `M`  | Combine ciphertexts using Bézout      | `e1x + e2y = 1` → `M = C1^x · C2^y mod n` ([Cryptography Stack Exchange][1]) |
| **Håstad Broadcast Attack**       | Same `M`, small `e`, different `n` | Use CRT to reconstruct `M^e`          | `M = √[e]{CRT(C1,...,Ce)}`                                                   |
| **Generalized Håstad**            | Related messages `(M+k)`           | Solve structured polynomial system    | `(M+k)^e ≡ C mod n`                                                          |
| **Common Factor (GCD)**           | Shared primes across keys          | Compute `gcd(n1, n2)`                 | `p = gcd(n1, n2)`                                                            |
| **Wiener Attack**                 | Very small `d`                     | Continued fractions recover `d`       | `d < n^0.25`                                                                 |
| **Boneh–Durfee**                  | Small `d` (but not tiny)           | Lattice attack (LLL)                  | `d < n^0.292`                                                                |
| **dp Leak Attack**                | Given `dp = d mod (p−1)`           | Recover `p` using relation            | `edp ≡ 1 mod (p−1)`                                                          |
| **Partial d Exposure**            | Some bits of `d` known             | Use Coppersmith                       | `ed − kφ(n) = 1`                                                             |
| **Coppersmith (General)**         | Small unknown values               | Find small roots of polynomial        | `f(x) ≡ 0 mod n`                                                             |
| **Franklin–Reiter**               | Related messages known             | Polynomial GCD attack                 | `gcd(f(x), g(x)) → root`                                                     |
| **Short Pad Attack**              | Small random padding               | Brute Δ → reduce to FR                | `(x+r)^e`                                                                    |
| **Known Prefix Attack**           | Prefix known, suffix small         | Small root recovery                   | `(A + x)^e ≡ C mod n`                                                        |
| **CRT Attack (Low e reuse)**      | Same `M`, small `e`                | Combine ciphertexts                   | `CRT → M^e`                                                                  |
| **LSB Oracle Attack**             | Oracle leaks `M mod 2`             | Binary search on plaintext            | `M·2^i mod n`                                                                |
| **Bleichenbacher Attack**         | PKCS#1 v1.5 padding oracle         | Interval narrowing                    | `2B ≤ M < 3B`                                                                |
| **Manger Attack**                 | OAEP + comparison oracle           | Boundary-based narrowing              | `M·s mod n < B`                                                              |
| **Timing Attack**                 | Time leaks info                    | Recover bits of `d`                   | Square-and-multiply timing                                                   |
| **Fault Attack**                  | Faulty CRT computation             | Compare faulty output                 | `gcd(M − M', n)`                                                             |
| **Multiplicative Attack**         | No padding                         | Exploit homomorphism                  | `E(M1)·E(M2)=E(M1M2)`                                                        |
| **Replay / Deterministic Attack** | No padding                         | Same message → same ciphertext        | `C = M^e mod n`                                                              |


# 🧠 Key Unifying Formulas

These explain **almost all attacks**:

### 1. RSA Definition

```text
C = M^e mod n
M = C^d mod n
```

---

### 2. Key Equation

```text
ed ≡ 1 mod φ(n)
```

---

### 3. Multiplicative Property

```text
E(M1) · E(M2) = E(M1 · M2)
```

→ Used in:

```text
LSB, Bleichenbacher, Manger, chosen-ciphertext attacks
```

---

### 4. Small Root Form

```text
f(x) ≡ 0 mod n
```

→ Used in:

```text
Coppersmith, known prefix, partial d, short pad
```

---

### 5. CRT Combination

```text
x ≡ ai mod ni
```

→ Used in:

```text
Håstad, broadcast, CRT attacks
```

---

# 🧩 How to Think in CTFs (Important)

Instead of memorizing attacks, map problem → pattern:

| Pattern                 | Attack                        |
| ----------------------- | ----------------------------- |
| Same `n`, different `e` | Common modulus                |
| Same `M`, small `e`     | Håstad                        |
| Close primes            | Fermat                        |
| Small `d`               | Wiener / Boneh–Durfee         |
| Partial info            | Coppersmith                   |
| Oracle access           | LSB / Bleichenbacher / Manger |
| Bad padding             | Padding attacks               |
| Shared primes           | GCD                           |

---

# ✅ Final Note

You’ve basically covered:

```text
All major RSA attack families:
- Algebraic
- Lattice
- Oracle
- Implementation
```

At this point, you’re not “learning attacks” anymore —
you’re recognizing **patterns of broken assumptions**.

