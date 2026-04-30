# Hybrid Attack

## What is a Hybrid Attack?
A **hybrid attack** combines a dictionary attack with brute force — it takes wordlist entries and appends/prepends brute-forced characters. It targets the common pattern of `word + numbers/symbols`.

```
"password" + "123"  → "password123"
"summer"   + "2024" → "summer2024"
"dragon"   + "!"    → "dragon!"
```

---

## How It Works

```
Wordlist word → apply brute force mask → try hash

"password" + ?d?d?d → password000 ... password999
"letmein"  + ?d?d   → letmein00  ... letmein99
```

---

## Hashcat Hybrid Modes

```bash
# Mode 6: Wordlist + Mask (append)
hashcat -m 0 -a 6 hashes.txt rockyou.txt ?d?d?d?d

# Mode 7: Mask + Wordlist (prepend)
hashcat -m 0 -a 7 hashes.txt ?d?d?d?d rockyou.txt

# Examples:
hashcat -m 0 -a 6 hashes.txt words.txt ?d?d         # word + 2 digits
hashcat -m 0 -a 6 hashes.txt words.txt ?d?d?d?d     # word + 4 digits (year)
hashcat -m 0 -a 6 hashes.txt words.txt ?s           # word + symbol
hashcat -m 0 -a 6 hashes.txt words.txt ?u?l?l?d     # word + upper+lower+lower+digit

# Masks:
# ?l = lowercase a-z
# ?u = uppercase A-Z
# ?d = digit 0-9
# ?s = special !@#$...
# ?a = all printable
```

---

## Python Example

```python
import hashlib, itertools, string

def hybrid_attack(target: str, wordlist: list, suffix_len: int = 3):
    charset = string.digits
    for word in wordlist:
        for suffix in itertools.product(charset, repeat=suffix_len):
            candidate = word + ''.join(suffix)
            if hashlib.sha256(candidate.encode()).hexdigest() == target:
                return candidate
    return None

target = hashlib.sha256(b"summer123").hexdigest()
result = hybrid_attack(target, ["summer", "winter", "password"])
print(result)  # "summer123"
```

---

## Defense
- Use **bcrypt/Argon2** — makes each attempt slow
- Block passwords matching `word + digits` patterns
- Enforce **minimum length of 12+** characters
- Use **passphrases** instead of word+number combos
