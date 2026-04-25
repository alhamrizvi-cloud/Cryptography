
# 📘 1. CORE VALUE RECOVERY (ALWAYS FIRST)

## 🔹 If you can factor `n`

```python
from sympy import factorint, mod_inverse

n = ...
e = ...
C = ...

fac = factorint(n)
p, q = list(fac.keys())

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)

M = pow(C, d, n)

print("p =", p)
print("q =", q)
print("d =", d)
print("M =", M)
```

---

## 🔹 If you already have `p` and `q`

```python
from sympy import mod_inverse

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)

M = pow(C, d, n)
```

---

## 🔹 If you have `d`

```python
M = pow(C, d, n)
```

---

## 🔹 If you have `dp`

```python
from sympy import gcd

for k in range(1, e):
    if (e*dp - 1) % k == 0:
        p = (e*dp - 1)//k + 1
        if n % p == 0:
            q = n // p
            break
```

---

## 🔹 If two moduli share a prime

```python
from math import gcd

p = gcd(n1, n2)
q = n1 // p
```

---

# ⚡ 2. ATTACK SCRIPTS (ALL IMPORTANT ONES)

---

# 🔓 Fermat Attack

```python
import math

n = ...

a = math.isqrt(n)
if a*a < n:
    a += 1

while True:
    b2 = a*a - n
    b = math.isqrt(b2)

    if b*b == b2:
        break
    a += 1

p = a - b
q = a + b

print(p, q)
```

---

# 🔗 Common Modulus

```python
from sympy import gcdex, mod_inverse

x, y, _ = gcdex(e1, e2)

if x < 0:
    C1 = mod_inverse(C1, n)
    x = -x

if y < 0:
    C2 = mod_inverse(C2, n)
    y = -y

M = (pow(C1, x, n) * pow(C2, y, n)) % n
print(M)
```

---

# 📡 Håstad Broadcast

```python
from sympy.ntheory.modular import crt
import sympy

c, _ = crt(n_list, c_list)
m = int(sympy.integer_nthroot(c, e)[0])

print(m)
```

---

# 🧠 Wiener Attack

```python
from sympy import Rational

def cont_frac(n, d):
    cf = []
    while d:
        q = n // d
        cf.append(q)
        n, d = d, n - q*d
    return cf

def convergents(cf):
    conv = []
    for i in range(len(cf)):
        num, den = 1, 0
        for q in reversed(cf[:i+1]):
            num, den = den + num*q, num
        conv.append((num, den))
    return conv

cf = cont_frac(e, n)

for k, d in convergents(cf):
    if k == 0:
        continue
    if (e*d - 1) % k == 0:
        print("Found d:", d)
```

---

# 🔑 dp Leak

```python
from sympy import mod_inverse

A = e*dp - 1

for k in range(1, e):
    if A % k == 0:
        p = A//k + 1
        if n % p == 0:
            q = n // p
            break
```

---

# 🧩 Franklin-Reiter

```python
from sympy import symbols, gcd

x = symbols('x')

f1 = (x)**e - C1
f2 = (x + k)**e - C2

g = gcd(f1, f2)

print(g)
```

---

# 🔐 Known Prefix (Coppersmith-style simple)

```python
# brute small unknown part
for x in range(1000000):
    m = known_prefix + x
    if pow(m, e, n) == C:
        print(m)
        break
```

---

# 🔄 LSB Oracle

```python
low = 0
high = n

for i in range(n.bit_length()):
    C = (C * pow(2, e, n)) % n
    bit = oracle(C)

    mid = (low + high) // 2
    if bit == 0:
        high = mid
    else:
        low = mid

print(low)
```

---

# 🧨 Fault Attack

```python
from math import gcd

p = gcd(correct_M - faulty_M, n)
q = n // p
```

---

# 🧠 CRT Attack (manual)

```python
from sympy.ntheory.modular import crt

m, _ = crt(n_list, c_list)
```

---

# 🧩 Short Pad (brute Δ)

```python
for r in range(10000):
    m = ...
    if pow(m + r, e, n) == C:
        print(m)
```

---

# ⚠️ 3. WHAT YOU SHOULD ALWAYS DO FIRST

```python
# 1. Try factor
factorint(n)

# 2. Check gcd with other n
gcd(n1, n2)

# 3. Check small e
# 4. Check same modulus
# 5. Check multiple ciphertexts
```

---

# 🧠 FINAL WORKFLOW (REAL USE)

```text
1. Try factor → get p,q → done
2. If fail → check reuse (n / M)
3. If fail → check small values
4. If fail → check structure
5. If fail → check oracle
```
