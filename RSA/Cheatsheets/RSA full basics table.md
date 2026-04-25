
# 📘 RSA CHEAT SHEET (FULL DECISION + FORMULAS)

# 🔑 1. Core RSA Setup

| Concept        | Formula             |
| -------------- | ------------------- |
| Key generation | `n = p · q`         |
| Totient        | `φ(n) = (p−1)(q−1)` |
| Public key     | `(n, e)`            |
| Private key    | `d = e⁻¹ mod φ(n)`  |
| Encryption     | `C = M^e mod n`     |
| Decryption     | `M = C^d mod n`     |


# 🧠 2. Core Properties (VERY IMPORTANT)

| Property                   | Meaning                                |
| -------------------------- | -------------------------------------- |
| Multiplicative             | `E(a)·E(b) = E(ab)`                    |
| Deterministic (no padding) | Same message → same ciphertext         |
| CRT optimization           | Faster decryption using `dp`, `dq`     |
| Structure preserving       | Algebraic relations survive encryption |


# ⚡ 3. Quick Decision Table (WHAT TO DO)

| Given Situation               | Attack          |
| ----------------------------- | --------------- |
| Small `n`                     | Factor it       |
| `p ≈ q`                       | Fermat          |
| Same `n`, different `e`       | Common modulus  |
| Same `M`, small `e`, diff `n` | Håstad          |
| Related messages              | Franklin-Reiter |
| Small padding                 | Short pad       |
| Known prefix                  | Coppersmith     |
| Small `d`                     | Wiener          |
| Medium-small `d`              | Boneh–Durfee    |
| `dp` or `dq` given            | dp leak         |
| Partial key known             | Coppersmith     |
| Oracle (bit leak)             | LSB             |
| Oracle (padding)              | Bleichenbacher  |
| OAEP oracle                   | Manger          |
| Timing info                   | Timing attack   |
| Shared primes                 | GCD             |
| Faulty computation            | Fault attack    |


# 🔍 4. Factoring-Based Attacks

| Attack          | Formula           |
| --------------- | ----------------- |
| Basic factoring | `n = p·q`         |
| Fermat          | `n = a² − b²`     |
| GCD attack      | `p = gcd(n1, n2)` |


# 📡 5. Broadcast / Multi-Use

| Attack             | Formula                      |
| ------------------ | ---------------------------- |
| Håstad             | `M = √[e]{CRT(C1, C2, ...)}` |
| Generalized Håstad | `(M + k)^e`                  |

---

# 🔗 6. Common Modulus

| Step    | Formula                 |
| ------- | ----------------------- |
| Solve   | `e1x + e2y = 1`         |
| Recover | `M = C1^x · C2^y mod n` |


# 🧩 7. Small Root / Coppersmith Family

| Case         | Formula               |
| ------------ | --------------------- |
| Known prefix | `(A + x)^e ≡ C mod n` |
| Partial d    | `e(d0 + x) − 1 ≡ 0`   |
| Short pad    | `(M + r)^e`           |
| General form | `f(x) ≡ 0 mod n`      |


# 🔐 8. Small Private Key Attacks

| Attack       | Condition     | Formula             |
| ------------ | ------------- | ------------------- |
| Wiener       | `d < n^0.25`  | Continued fractions |
| Boneh–Durfee | `d < n^0.292` | Lattice (LLL)       |


# 🧮 9. CRT / Key Leakage

| Attack  | Formula                |
| ------- | ---------------------- |
| dp leak | `p = (e·dp − 1)/k + 1` |
| dq leak | same for `q`           |
| CRT     | combine mod `p`, `q`   |


# 🔄 10. Related Message Attacks

| Attack          | Formula           |
| --------------- | ----------------- |
| Franklin-Reiter | `gcd(f(x), g(x))` |
| Short pad       | brute Δ → FR      |
| Known relation  | `M2 = aM1 + b`    |

# 🔓 11. Oracle Attacks

## LSB Oracle

| Step   | Formula            |
| ------ | ------------------ |
| Modify | `C' = C·2^e mod n` |
| Result | `M' = 2M mod n`    |


## Bleichenbacher

| Condition     | Formula       |
| ------------- | ------------- |
| Valid padding | `2B ≤ M < 3B` |

## Manger

| Condition      | Formula         |
| -------------- | --------------- |
| Boundary check | `M·s mod n < B` |

# 🧠 12. Side-Channel Attacks

| Attack | Idea                    |
| ------ | ----------------------- |
| Timing | Bit-dependent execution |
| Power  | Power usage leaks       |
| Cache  | Memory access leaks     |

# ⚠️ 13. Implementation Failures

| Problem        | Result                 |
| -------------- | ---------------------- |
| No padding     | deterministic → broken |
| Bad RNG        | weak primes            |
| Reused primes  | GCD attack             |
| Partial checks | padding oracle         |
| CRT faults     | factorization          |

# 📐 14. Important Constants

| Symbol | Meaning          |
| ------ | ---------------- |
| `n`    | modulus          |
| `e`    | public exponent  |
| `d`    | private exponent |
| `φ(n)` | totient          |
| `B`    | padding bound    |
| `k`    | byte length      |


# 🧩 15. Universal Attack Patterns

| Pattern             | Meaning             |
| ------------------- | ------------------- |
| Same input reused   | exploit determinism |
| Structure preserved | algebra attack      |
| Small value         | brute / Coppersmith |
| Oracle access       | adaptive attack     |
| Weak randomness     | factorization       |


# 🧠 16. Mental Model (IMPORTANT)

All RSA attacks reduce to:

```text
1. Factor n
2. Recover d
3. Solve small equation
4. Exploit structure
5. Abuse oracle
```


# 🚀 17. What To Do in CTF (FAST THINK)

```text
1. Check n → factor?
2. Check reuse → same n / same M?
3. Check size → small d / small e?
4. Check structure → prefix / relation?
5. Check oracle → responses?
6. Check leak → dp / bits?
```

