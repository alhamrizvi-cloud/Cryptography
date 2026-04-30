# Avalanche Effect

## What is the Avalanche Effect?
The **avalanche effect** is a desirable property of cryptographic functions where a small change in input (even a single bit) produces a drastically different output (approximately 50% of output bits change). Named by cryptographer Horst Feistel.

```
Input:  "Hello"    → SHA-256 → a948eb... 
Input:  "hello"    → SHA-256 → 2cf24d...
                              ↑ Completely different!
```

---

## Why the Avalanche Effect Matters

Without it, attackers could:
- Learn information about the input from similar outputs
- Use differential cryptanalysis to break the cipher
- Predict hash outputs from small input changes
- Narrow down password guesses from near-matches

**A weak avalanche effect** = **cryptographic weakness**

---

## Measuring the Avalanche Effect

For an ideal hash: flipping **1 bit** in input should flip ~**50% of output bits**

```python
import hashlib

def bit_difference(h1: str, h2: str) -> float:
    """Count percentage of bits that differ between two hex hashes"""
    b1 = bin(int(h1, 16))[2:].zfill(len(h1) * 4)
    b2 = bin(int(h2, 16))[2:].zfill(len(h2) * 4)
    different = sum(a != b for a, b in zip(b1, b2))
    return different / len(b1) * 100

h1 = hashlib.sha256(b"Hello").hexdigest()
h2 = hashlib.sha256(b"hello").hexdigest()

print(f"SHA-256 of 'Hello': {h1}")
print(f"SHA-256 of 'hello': {h2}")
print(f"Bits different: {bit_difference(h1, h2):.1f}%")
# → approximately 50% (near-ideal avalanche)
```

---

## Avalanche in Hash Functions

### SHA-256 Example
```
Input:  "The quick brown fox"
Hash:   d9014c4624844aa5bac314773d6b689ad467fa4e1d1a50a1b8a99d5a95f72ff5

Input:  "The quick brown Fox"  (only 'f' changed to 'F')
Hash:   a48b36ccf069bfe5f11f7e1d3e1f96b44f0c3a3adbb96e7e43e4ac4c26f7f97c
        ↑ Almost entirely different output!
```

### Bit-Level Analysis
```
"fox" → hash bit pattern: 11010110 00101101 ...
"Fox" → hash bit pattern: 01001001 11010010 ...
                          ↑↑↑↑↑↑↑↑ ↑↑ ↑↑ ↑↑
                          Most bits changed!
```

---

## Avalanche in Block Ciphers

### AES Avalanche
```
Key:    00000000 00000000 00000000 00000000
Plain:  00000000 00000000 00000000 00000000
Cipher: 66e94bd4 ef8a2c3b 884cfa59 ca342b2e

Key:    00000000 00000000 00000000 00000001 (1 bit changed!)
Plain:  00000000 00000000 00000000 00000000
Cipher: 58e2fccefa7e3061367f1d57a4e7455a (completely different!)
```

AES achieves near-perfect avalanche through:
1. **SubBytes**: Nonlinear S-box substitution
2. **ShiftRows**: Row permutation
3. **MixColumns**: Linear mixing (ensures all 4 bytes interact)
4. **AddRoundKey**: XOR with round key

---

## Strict Avalanche Criterion (SAC)

Formal definition: A function satisfies SAC if:
- For every single-bit input flip
- Exactly 50% of output bits change on average

```
f satisfies SAC ↔ ∀i: Prob[f(x)_j ≠ f(x ⊕ eᵢ)_j] = 1/2  for all j
```

---

## Visualizing Avalanche Effect

```
Single-bit flip cascade in SHA-256 compression function:

Input bit 0 flipped
↓
Step 1: Affects one word of state
↓
Step 2: XOR/ADD operations spread to 2+ words
↓
Step 10: Affects 4+ words
↓
Step 30: All 8 words of state affected
↓
Step 64: Nearly all output bits changed (~50%)
```

---

## Avalanche Effect in Passwords

```
Password: "secret123"  →  bcrypt hash: $2b$12$AAA...1234abcd
Password: "secret124"  →  bcrypt hash: $2b$12$AAA...9876efgh
                                                ↑↑↑ totally different!

You CANNOT determine similarity of passwords from their hashes.
```

This is why:
- Changing one character changes the entire hash
- An attacker who sees your hash learns nothing about similar passwords
- "Close" passwords don't produce "close" hashes

---

## Poor Avalanche: Real-World Failure Examples

### CRC32 (Not Cryptographic!)
```
CRC32("Hello") = 0xF7D18982
CRC32("Jello") = 0xB35843F9
→ Only ~50% bits differ — but achievable by design
→ NOT suitable for cryptographic use!
```

### Linear Hash (Hypothetical Bad Design)
```
bad_hash(x) = (x * 1234567) mod 2^32
bad_hash(100) = 123456700
bad_hash(101) = 123457934  ← Only slightly different!
→ Almost no avalanche — completely insecure
```

---

## Testing Avalanche Effect

```python
import hashlib

def test_avalanche(data: bytes, algorithm: str = 'sha256') -> dict:
    """Test avalanche effect by flipping each bit"""
    h = hashlib.new(algorithm)
    h.update(data)
    original_hash = h.hexdigest()
    original_bits = bin(int(original_hash, 16))[2:].zfill(
        hashlib.new(algorithm).digest_size * 8
    )
    
    bit_changes = []
    for byte_idx in range(len(data)):
        for bit_idx in range(8):
            # Flip one bit
            modified = bytearray(data)
            modified[byte_idx] ^= (1 << bit_idx)
            
            h2 = hashlib.new(algorithm)
            h2.update(bytes(modified))
            new_hash = h2.hexdigest()
            new_bits = bin(int(new_hash, 16))[2:].zfill(len(original_bits))
            
            # Count changed bits
            changed = sum(a != b for a, b in zip(original_bits, new_bits))
            bit_changes.append(changed / len(original_bits) * 100)
    
    return {
        "min_change": min(bit_changes),
        "max_change": max(bit_changes),
        "avg_change": sum(bit_changes) / len(bit_changes),
        "target": 50.0
    }

result = test_avalanche(b"Hello")
print(f"Average bit change: {result['avg_change']:.1f}%")  # ~50%
print(f"Min bit change: {result['min_change']:.1f}%")
print(f"Max bit change: {result['max_change']:.1f}%")
```

---

## Algorithms and Their Avalanche Quality

| Algorithm | Avg Bit Change | SAC Compliant | Cryptographic |
|-----------|---------------|---------------|---------------|
| SHA-256 | ~50% | ✅ Yes | ✅ Yes |
| SHA-3 | ~50% | ✅ Yes | ✅ Yes |
| AES | ~50% | ✅ Yes | ✅ Yes |
| MD5 | ~50% | ✅ Yes | ❌ Broken (collisions) |
| CRC32 | ~30-50% | ❌ No | ❌ Not crypto |
| Caesar Cipher | 0% | ❌ No | ❌ Not crypto |
| XOR cipher | 0% | ❌ No | ❌ Not crypto |

---

## Best Practices
- Choose hash functions/ciphers with **proven avalanche properties** (SHA-256, AES)
- When implementing custom crypto (rare and discouraged): test for SAC compliance
- The avalanche effect is why you **cannot** recover password similarity from hashes
- Lack of avalanche is a red flag for any proposed cryptographic primitive
