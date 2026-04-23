
# RSA Cheat Sheet (Compact Comparison)

| Topic           | Mathematical Formula  | Python Equivalent       |
| --------------- | --------------------- | ----------------------- |
| Primes          | p, q                  | `p = ...`, `q = ...`    |
| Modulus         | n = p × q             | `n = p * q`             |
| Totient         | φ(n) = (p − 1)(q − 1) | `phi = (p - 1)*(q - 1)` |
| GCD Check       | gcd(e, φ(n)) = 1      | `math.gcd(e, phi)`      |
| Public Exponent | 1 < e < φ(n)          | `e = ...`               |
| Private Key     | d ≡ e⁻¹ mod φ(n)      | `mod_inverse(e, phi)`   |
| Public Key      | (e, n)                | `(e, n)`                |
| Private Key     | (d, n)                | `(d, n)`                |
| Encryption      | C = M^e mod n         | `pow(M, e, n)`          |
| Decryption      | M = C^d mod n         | `pow(C, d, n)`          |
| Mod Operation   | a mod n               | `a % n`                 |
| Fast Exponent   | a^b mod n             | `pow(a, b, n)`          |
| Factorization   | n → p × q             | `factorint(n)`          |

---

## Minimal Full Flow

| Step    | Mathematical Form               | Python Code  |
| ------- | ------------------------------- | ------------ |
| Key Gen | n = p×q, φ(n), d ≡ e⁻¹ mod φ(n) | see below    |
| Encrypt | C = M^e mod n                   | `pow(M,e,n)` |
| Decrypt | M = C^d mod n                   | `pow(C,d,n)` |

```python
from sympy import mod_inverse

p, q = 61, 53
e = 17
M = 42

n = p * q
phi = (p - 1)*(q - 1)
d = mod_inverse(e, phi)

C = pow(M, e, n)
M_dec = pow(C, d, n)
```

