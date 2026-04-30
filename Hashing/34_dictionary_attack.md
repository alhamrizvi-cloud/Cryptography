# Dictionary Attack

## What is a Dictionary Attack?
A **dictionary attack** tries a precompiled list of likely passwords (a "dictionary" or wordlist) rather than every possible combination. It exploits the fact that humans choose predictable, meaningful passwords.

```
Wordlist: ["password", "123456", "letmein", "qwerty", ...]
For each word: if H(word) == target → FOUND!
```

---

## Why Dictionary Attacks Work

- 85%+ of users choose passwords from a limited, predictable set
- People use words, names, dates, sports teams, keyboard patterns
- Even with complexity rules, people do predictable mutations:
  - `password` → `P@ssw0rd`
  - `summer` → `Summer2023!`

---

## Common Password Statistics

```
Top 10 most used passwords (2023):
1. 123456
2. password
3. 123456789
4. 12345
5. 1234567890
6. qwerty
7. password1
8. abc123
9. 111111
10. 123123
```

These are cracked **instantly** in any dictionary attack.

---

## Wordlist Sources

### Built-in with Tools
```
/usr/share/wordlists/rockyou.txt   ← 14 million real passwords (from 2009 RockYou breach)
/usr/share/wordlists/fasttrack.txt ← Fast common passwords
SecLists (GitHub)                   ← Huge collection of wordlists
```

### RockYou Wordlist
```
14,341,564 unique passwords
Real passwords from the 2009 RockYou breach
Most popular starting wordlist for attackers
```

### Custom Wordlists
- Target-specific: company name, employee names, city, sports team
- OSINT-derived: LinkedIn, social media, company website keywords

---

## Attack Speed vs Hash Type

| Hash | Speed (GPU RTX 4090) | RockYou done in |
|------|---------------------|-----------------|
| MD5 | 50B/sec | 0.0003 ms |
| SHA-256 | 8B/sec | 0.002 ms |
| SHA-1 | 20B/sec | 0.0007 ms |
| bcrypt (cost=12) | 12K/sec | ~20 minutes |
| Argon2id | ~300/sec | ~13 hours |

---

## Implementation Examples

### Python: Basic Dictionary Attack
```python
import hashlib

def dictionary_attack(target_hash: str, wordlist_path: str) -> str | None:
    """Try every word in a wordlist against a SHA-256 hash"""
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            word = line.strip()
            h = hashlib.sha256(word.encode()).hexdigest()
            if h == target_hash:
                return word
    return None

target = hashlib.sha256(b"letmein").hexdigest()
result = dictionary_attack(target, "/usr/share/wordlists/rockyou.txt")
print(f"Found: {result}")
```

### Python: Dictionary Attack with Mutations
```python
import hashlib

def mutate_word(word: str):
    """Generate common password mutations"""
    yield word
    yield word.capitalize()
    yield word.upper()
    yield word + "1"
    yield word + "123"
    yield word + "!"
    yield word + "2023"
    yield word + "2024"
    yield word[0].upper() + word[1:]
    yield word.replace('a', '@').replace('e', '3').replace('o', '0').replace('i', '1')
    yield word.capitalize() + "!"
    yield word.capitalize() + "1"
    yield word.capitalize() + "123!"

def mutated_dictionary_attack(target_hash: str, wordlist: list) -> str | None:
    for word in wordlist:
        for mutation in mutate_word(word):
            h = hashlib.sha256(mutation.encode()).hexdigest()
            if h == target_hash:
                return mutation
    return None

# Test
target = hashlib.sha256(b"P@ssword").hexdigest()
wordlist = ["password", "letmein", "qwerty", "dragon"]
result = mutated_dictionary_attack(target, wordlist)
print(f"Found: {result}")  # "P@ssword"
```

### Using Hashcat
```bash
# Basic dictionary attack
hashcat -m 0 -a 0 hashes.txt rockyou.txt

# Dictionary + rules (mutations)
hashcat -m 0 -a 0 hashes.txt rockyou.txt -r rules/best64.rule

# Dictionary + bcrypt
hashcat -m 3200 -a 0 bcrypt_hashes.txt rockyou.txt

# Dictionary + Argon2
hashcat -m 13400 -a 0 argon2_hashes.txt rockyou.txt

# Multiple wordlists
hashcat -m 0 -a 0 hashes.txt wordlist1.txt wordlist2.txt

# Show cracked passwords
hashcat -m 0 hashes.txt --show
```

### Using John the Ripper
```bash
# Dictionary attack with john
john --wordlist=rockyou.txt --format=sha256 hashes.txt

# With mutation rules
john --wordlist=rockyou.txt --rules=Jumbo --format=sha256 hashes.txt

# Show cracked
john --show hashes.txt

# Custom rules in john.conf:
# [List.Rules:Custom]
# $[0-9]          # Append digit 0-9
# ^[0-9]          # Prepend digit
# sa@             # Substitute a → @
```

---

## Hashcat Rule Files

Rules transform wordlist entries on-the-fly:

```bash
# Common rules
hashcat -m 0 hash.txt rockyou.txt -r rules/best64.rule
hashcat -m 0 hash.txt rockyou.txt -r rules/OneRuleToRuleThemAll.rule
hashcat -m 0 hash.txt rockyou.txt -r rules/Hob0Rules.rule
```

### Custom Rule Syntax
```
:          Do nothing (passthrough)
l          Lowercase all
u          Uppercase all
c          Capitalize
r          Reverse
d          Duplicate
$X         Append character X
^X         Prepend character X
[          Remove first character
]          Remove last character
sXY        Substitute X with Y
sa@        Substitute 'a' with '@'
se3        Substitute 'e' with '3'

# Example: password → P@ssw0rd
c sa@ se3 so0
```

---

## Credential Stuffing (Related Attack)

A special dictionary attack using **breached credentials**:

```
1. Attacker obtains breached username:password database
   (from HaveIBeenPwned, dark web, previous breaches)
2. Tests each pair against target site
3. People reuse passwords → immediate account takeover

Tool: Snipr, OpenBullet, SentryMBA (used by attackers)
Defense: MFA, breach monitoring, credential stuffing detection
```

---

## Generating Custom Wordlists

```bash
# CeWL - generates wordlist from target website
cewl https://targetcompany.com -m 6 -d 2 -w company_words.txt

# CUPP - custom user password profiler
python3 cupp.py -i  # Prompts for target's personal info

# Crunch - generate by pattern
crunch 8 8 -t @@@@2024 -o wordlist.txt  # Four letters + "2024"

# Mentalist (GUI-based wordlist generator)
```

---

## Defenses Against Dictionary Attacks

| Defense | Effectiveness |
|---------|--------------|
| Use bcrypt/Argon2 | High — makes each word attempt very slow |
| Salting | High — prevents precomputed lookups |
| Password policy (no common passwords) | High |
| HaveIBeenPwned check on signup | High |
| MFA | Excellent — even if password cracked, can't log in |
| Breach monitoring | Good — detect if credentials leaked |

---

## Best Practices
- Block passwords found in common wordlists at registration
- Integrate with **HaveIBeenPwned API** to block breached passwords:

```python
import hashlib, requests

def is_pwned(password: str) -> int:
    """Returns number of times password has appeared in breaches"""
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    
    r = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    for line in r.text.splitlines():
        h, count = line.split(':')
        if h == suffix:
            return int(count)
    return 0

count = is_pwned("password")
print(f"Seen {count} times in breaches")  # Millions!
```
