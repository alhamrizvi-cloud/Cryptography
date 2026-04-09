# Monoalphabetic Cipher & Permutation Cipher

## Overview

This repository explains classical cryptography techniques focusing on:

* Monoalphabetic Cipher
* Permutation Cipher
* Encryption & Decryption methods
* Frequency Analysis
* Brute-force and other cryptanalysis techniques
* Practical scripts

---

# 1. Monoalphabetic Cipher

## Definition

A **monoalphabetic cipher** is a substitution cipher where each letter in the plaintext is mapped to a fixed letter in the ciphertext.

Example mapping:

```
Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ
Cipher: QWERTYUIOPASDFGHJKLZXCVBNM
```

---

## Encryption

### Formula

```
C = E(P) = key[P]
```

### Example

```
Plaintext : HELLO
Key       : QWERTYUIOPASDFGHJKLZXCVBNM

H → I
E → T
L → S
L → S
O → G

Ciphertext: ITSSG
```

---

## Decryption

### Formula

```
P = D(C) = reverse_key[C]
```

Reverse mapping is required.

---

## Python Script (Monoalphabetic Cipher)

```python
import string

alphabet = string.ascii_uppercase
key = "QWERTYUIOPASDFGHJKLZXCVBNM"

enc_map = dict(zip(alphabet, key))
dec_map = dict(zip(key, alphabet))

def encrypt(text):
    return ''.join(enc_map.get(c, c) for c in text.upper())

def decrypt(text):
    return ''.join(dec_map.get(c, c) for c in text.upper())

# Example
print(encrypt("HELLO"))
print(decrypt("ITSSG"))
```

---

# 2. Permutation Cipher (Transposition Cipher)

## Definition

A **permutation cipher** rearranges the positions of characters instead of replacing them.

---

## Encryption

### Example (Key = 3 1 4 2)

Split into blocks:

```
Plaintext: HELLOWORLD
Blocks   : HELL OWOR LDXX
```

Reorder based on key:

```
Index: 1 2 3 4
Key  : 3 1 4 2

Rearranged block:
L H L E
```

---

## Python Script (Permutation Cipher)

```python
def encrypt_permutation(text, key):
    n = len(key)
    text = text.replace(" ", "").upper()
    
    while len(text) % n != 0:
        text += 'X'
    
    result = ""
    for i in range(0, len(text), n):
        block = text[i:i+n]
        result += ''.join(block[k-1] for k in key)
    
    return result

def decrypt_permutation(cipher, key):
    n = len(key)
    result = ""
    inv_key = [0]*n
    
    for i, k in enumerate(key):
        inv_key[k-1] = i
    
    for i in range(0, len(cipher), n):
        block = cipher[i:i+n]
        result += ''.join(block[inv_key[j]] for j in range(n))
    
    return result

key = [3,1,4,2]
cipher = encrypt_permutation("HELLO", key)
print(cipher)
print(decrypt_permutation(cipher, key))
```

---

# 3. Frequency Analysis

## Definition

Frequency analysis studies how often letters appear in ciphertext.

### English Letter Frequency (Approx)

```
E > T > A > O > I > N > S > H > R > D > L > U
```

---

## Frequency Analysis Script

```python
from collections import Counter

def frequency_analysis(text):
    text = text.upper()
    freq = Counter(c for c in text if c.isalpha())
    
    total = sum(freq.values())
    
    for letter, count in freq.most_common():
        print(f"{letter}: {count} ({count/total:.2%})")

frequency_analysis("ITSSG")
```

---

## Frequency Graph (Matplotlib)

```python
import matplotlib.pyplot as plt
from collections import Counter

def plot_frequency(text):
    text = text.upper()
    freq = Counter(c for c in text if c.isalpha())
    
    letters = sorted(freq.keys())
    counts = [freq[l] for l in letters]
    
    plt.bar(letters, counts)
    plt.xlabel("Letters")
    plt.ylabel("Frequency")
    plt.title("Letter Frequency Analysis")
    plt.show()

plot_frequency("ITSSG")
```

---

# 4. Cryptanalysis Techniques

## 1. Brute Force

Try all possible keys (limited practicality due to 26! possibilities).

```python
import itertools
import string

alphabet = string.ascii_uppercase

def brute_force(cipher):
    for perm in itertools.permutations(alphabet):
        key = ''.join(perm)
        dec_map = dict(zip(key, alphabet))
        plaintext = ''.join(dec_map.get(c, c) for c in cipher)
        
        if "THE" in plaintext:
            print(plaintext)
```

---

## 2. Frequency Matching

Map most frequent cipher letters to:

```
E, T, A, O, I
```

---

## 3. Known Plaintext Attack

If part of plaintext is known:

```
HELLO → ITSSG
H → I
E → T
```

---

## 4. Pattern Analysis

Example:

```
HELLO → pattern: 1-2-3-3-4
```

Used to match dictionary words.

---

## 5. Dictionary Attack

Compare decrypted outputs with English word lists.

---

# 5. Weaknesses

## Monoalphabetic Cipher

* Vulnerable to frequency analysis
* Fixed substitution makes patterns visible

## Permutation Cipher

* Letter frequency unchanged
* Can be broken using pattern recognition

---

# 6. Summary

| Technique      | Type          | Weakness                     |
| -------------- | ------------- | ---------------------------- |
| Monoalphabetic | Substitution  | Frequency analysis           |
| Permutation    | Transposition | Pattern & structure analysis |

---

# 7. Usage

Clone the repo and run:

```
python script.py
```

---

# 8. Notes

* Monoalphabetic cipher has **26! possible keys**
* Frequency analysis is the **most powerful attack**
* Permutation cipher keeps letter frequency intact


If you want, I can next upgrade this into a **full CTF toolkit repo (CLI tool with auto-decrypt, scoring, wordlists, etc.)**.
