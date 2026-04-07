# Caesar Cipher – Complete Notes

## 1. What is Caesar Cipher?

The **Caesar Cipher** is a **substitution cipher** where each letter in the plaintext is shifted by a fixed number of positions in the alphabet.

It is named after Julius Caesar, who used it to send secret messages.


## 2. Basic Idea

* Choose a number → called the **key (shift)**
* Shift each letter forward by that number

### Example (Key = 3)

```text
Plaintext:  HELLO
Ciphertext: KHOOR
```

Because:

```text
H → K (shift +3)
E → H
L → O
L → O
O → R
```



## 3. Alphabet Mapping

Alphabet is treated as circular:

```text
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
```

With shift = 3:

```text
A → D
B → E
C → F
...
X → A
Y → B
Z → C
```

---

## 4. Mathematical Representation

Convert letters to numbers:

```text
A = 0, B = 1, C = 2, ..., Z = 25
```

---

### Encryption Formula

```text
C = (P + k) mod 26
```

Where:

* `C` = ciphertext letter
* `P` = plaintext letter (number)
* `k` = key (shift)
* `mod 26` = wrap around alphabet

---

### Decryption Formula

```text
P = (C - k) mod 26
```

---

## 5. Example with Math

Encrypt **HELLO** with key = 3:

```text
H = 7 → (7 + 3) mod 26 = 10 → K
E = 4 → (4 + 3) = 7 → H
L = 11 → (11 + 3) = 14 → O
O = 14 → (14 + 3) = 17 → R
```

---

## 6. Encryption (Step-by-Step)

1. Choose key `k`
2. Convert each letter to number
3. Apply formula: `(P + k) mod 26`
4. Convert back to letters

---

## 7. Decryption (Step-by-Step)

1. Take ciphertext
2. Convert letters to numbers
3. Apply: `(C - k) mod 26`
4. Convert back to plaintext

---

## 8. Brute Force Attack

Since only **26 possible keys**, attacker can try all shifts:

```text
Key 1 → text
Key 2 → text
...
Key 25 → text
```

This is why Caesar Cipher is **not secure**.

---

## 9. Frequency Analysis

In English:

* Most common letter = **E**

If ciphertext has many `K`, maybe:

```text
K → E → shift = 6
```

This helps guess the key.

---

## 10. Python Implementation

### Encryption

```python id="caesar_enc_001"
def encrypt(text, k):
    result = ""
    for char in text:
        if char.isalpha():
            shift = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift + k) % 26 + shift)
        else:
            result += char
    return result
```

---

### Decryption

```python id="caesar_dec_002"
def decrypt(text, k):
    return encrypt(text, -k)
```

---

## 11. Brute Force Script

```python id="caesar_bruteforce_003"
def brute_force(text):
    for k in range(26):
        print(f"Key {k}: {encrypt(text, -k)}")
```

---

## 12. Key Points for CTFs

* If text looks like: `uryyb` → likely Caesar/ROT13
* Try:

```bash
tr 'a-zA-Z' 'n-za-mN-ZA-M'
```

* Use tools:

  * CyberChef
  * dcode.fr
* Look for readable English output

---

## 13. Limitations

* Very weak encryption
* Only 26 keys
* Easily broken with brute force or frequency analysis

---

## 14. Variants

* **ROT13** → special case where key = 13
* **Shift cipher** → general form of Caesar cipher

---

## Final Summary

* Caesar Cipher = shift letters
* Uses modular arithmetic (mod 26)
* Easy to implement, easy to break
* Important for understanding basic cryptography concepts

---

If you want, next I can give you:

* **Vigenère Cipher (next level)**
* or **how to detect Caesar instantly in CTFs (pro tricks)**
