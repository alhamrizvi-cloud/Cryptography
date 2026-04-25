
# Partial d Exposure Attack

## 1. Problem Setup

We are given:

```text
n = p · q
e = public exponent
```

But instead of full `d`, we know **part of it**:

```text
d = known_part + unknown_part
```

Example:

```text
Lower bits of d are known
Upper bits unknown
```

## 2. Core Idea

From RSA:

```text
e · d ≡ 1 mod φ(n)
```

Rewrite:

```text
e·d − 1 = k·φ(n)
```

Substitute:

```text
d = d0 + x
```

Where:

```text
d0 = known part
x  = unknown part
```

Then:

```text
e(d0 + x) − 1 = k·φ(n)
```

Rearrange:

```text
e·x = k·φ(n) − e·d0 + 1
```

## 3. Why this is useful

```text
x is small (unknown bits are few)
```

So we can:

```text
solve for x using lattice techniques
```

This is where **Coppersmith's Method** comes in.


## 4. Key Insight

```text
We reduce RSA to a small root problem
```

Instead of factoring `n`, we solve:

```text
f(x) ≡ 0 mod n
```

Where `x` is small.

---

## 5. When It Works

```text
If enough bits of d are known
```

Typical condition:

```text
Known bits ≥ ~50% of d
```

## 6. Attack Strategy

1. Express:

```text
d = d0 + x
```

2. Substitute into:

```text
e·d − 1 = k·φ(n)
```

3. Build polynomial in `x`

4. Use lattice (Coppersmith) to find small `x`

5. Recover full `d`

6. Decrypt normally

## 7. Python Reality

Important:

```text
This is NOT practical in plain Python
```

You need:

* **SageMath**
* or advanced lattice libraries

## 8. SageMath Script (Typical)

```python
# SageMath required

n = ...
e = ...
d0 = ...  # known part

PR.<x> = PolynomialRing(Zmod(n))

f = e*(d0 + x) - 1

# Find small root
roots = f.small_roots(X=2^kbits, beta=0.5)

print(roots)
```

## 9. Simpler Case (Bruteforce version)

If unknown part is very small:

```python
from sympy import mod_inverse

n = ...
e = ...
d0 = ...
bits = 8  # unknown bits

for x in range(2**bits):
    d = d0 + x
    if (e*d - 1) % n != 0:
        continue

    print("Found d:", d)
```

This only works if:

```text
Unknown bits are extremely small
```

## 10. When to Recognize in CTF

Look for:

```text
"partial key leaked"
"some bits of d known"
"d starts with..."
"d ends with..."
```

## 11. Why This Breaks RSA

Because:

```text
Even partial leakage reduces search space
```

And lattice methods exploit:

```text
small unknown variables
```

## 12. Important Variants

### Known MSB of d

```text
High bits known
```

### Known LSB of d

```text
Low bits known
```

### Mixed leakage

```text
Scattered bits known
```

All solvable with variations of Coppersmith.

## 13. Limitations

```text
Too few known bits → attack fails
Requires lattice math
Not beginner-friendly in raw form
```

## 14. Summary

```text
Partial d known → express d = d0 + x
→ build equation
→ solve small root (Coppersmith)
→ recover d
→ decrypt
```

