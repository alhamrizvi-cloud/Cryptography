# Binary

## What is Binary?
**Binary** is the base-2 number system using only digits `0` and `1`. It is the fundamental language of computers — all data (text, images, keys, hashes) is ultimately stored and processed as binary.

---

## Binary Basics

| Base | Digits | Example |
|------|--------|---------|
| Binary (2) | 0, 1 | `1010` |
| Octal (8) | 0–7 | `12` |
| Decimal (10) | 0–9 | `10` |
| Hex (16) | 0–9, A–F | `A` |

All represent the same value: **ten**

---

## Bit, Nibble, Byte

| Unit | Bits | Range | Hex digits |
|------|------|-------|-----------|
| Bit | 1 | 0–1 | — |
| Nibble | 4 | 0–15 | 1 |
| Byte | 8 | 0–255 | 2 |
| Word | 16 | 0–65535 | 4 |
| Dword | 32 | 0–4294967295 | 8 |
| Qword | 64 | 0–18446744073709551615 | 16 |

---

## Binary Conversion

### Binary → Decimal
```
1101 0110

Position: 7  6  5  4  3  2  1  0
Bit:       1  1  0  1  0  1  1  0
Value:   128 64  0 16  0  4  2  0

Sum: 128 + 64 + 16 + 4 + 2 = 214
```

### Decimal → Binary
```
214 ÷ 2 = 107 R 0
107 ÷ 2 =  53 R 1
 53 ÷ 2 =  26 R 1
 26 ÷ 2 =  13 R 0
 13 ÷ 2 =   6 R 1
  6 ÷ 2 =   3 R 0
  3 ÷ 2 =   1 R 1
  1 ÷ 2 =   0 R 1

Read remainders bottom-up: 11010110 = 214 ✓
```

### Binary ↔ Hex
```
Group binary into nibbles (4 bits):
1101 0110
 D    6     → 0xD6
```

---

## Bitwise Operations (Critical in Cryptography)

| Operation | Symbol | Description |
|-----------|--------|-------------|
| AND | `&` | Both bits 1 → 1 |
| OR | `\|` | Either bit 1 → 1 |
| XOR | `^` | Bits differ → 1 |
| NOT | `~` | Flip all bits |
| Left Shift | `<<` | Multiply by 2^n |
| Right Shift | `>>` | Divide by 2^n |

### XOR (Most Important in Crypto)
```
A XOR B = C
C XOR B = A    ← XOR is its own inverse!
C XOR A = B

0 XOR 0 = 0
0 XOR 1 = 1
1 XOR 0 = 1
1 XOR 1 = 0    ← Both same = 0

Key XOR Plaintext  = Ciphertext
Ciphertext XOR Key = Plaintext    ← Used in stream ciphers, OTP
```

### AND (Masking)
```
10110101 AND
11110000 (mask)
──────────────
10110000        ← Extracts upper nibble
```

### OR (Setting Bits)
```
10110000 OR
00001111
──────────────
10111111        ← Sets lower nibble bits
```

---

## Binary in Cryptography

### One-Time Pad (OTP)
```
Plaintext:  01001000 01100101  ("He")
Key:        10110110 00101100  (random)
XOR:
Ciphertext: 11111110 01001001  (unbreakable if key is truly random)

Decrypt: Ciphertext XOR Key = Plaintext
```

### Stream Cipher
```
Key Stream: 10101010 10101010 ...
Plaintext:  01001000 01100101 ...
XOR:
Ciphertext: 11100010 11001111 ...
```

### AES Key Expansion (uses XOR heavily)
```
Round key XOR state at each AES round
```

### Hash Functions
```
SHA-256 uses:
- XOR (⊕)
- AND (&)
- OR (|)
- NOT (~)
- Bit rotation (ROTR)
- Addition modulo 2^32
```

---

## Implementation Examples

### Python
```python
# Integer to binary string
bin(214)          # '0b11010110'
format(214, 'b')  # '11010110'
format(214, '08b') # '11010110' (zero-padded to 8 bits)

# Binary string to integer
int('11010110', 2)  # 214

# Bytes to binary
def bytes_to_bin(data: bytes) -> str:
    return ' '.join(format(b, '08b') for b in data)

bytes_to_bin(b"Hi")
# '01001000 01101001'

# Bitwise XOR on bytes
a = bytes([0b10101010, 0b11001100])
b = bytes([0b01010101, 0b00110011])
xored = bytes(x ^ y for x, y in zip(a, b))

# XOR two byte strings (stream cipher style)
def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

# Bit operations
x = 0b10110101
upper_nibble = (x >> 4) & 0x0F   # 11
lower_nibble = x & 0x0F           # 5
set_bit = x | (1 << 3)            # set bit 3
clear_bit = x & ~(1 << 3)         # clear bit 3
toggle_bit = x ^ (1 << 3)         # toggle bit 3
check_bit = (x >> 3) & 1          # check bit 3
```

### JavaScript
```javascript
// Binary representations
(214).toString(2);           // '11010110'
parseInt('11010110', 2);     // 214

// Padding
(214).toString(2).padStart(8, '0'); // '11010110'

// Bitwise ops
const a = 0b10101010;
const b = 0b11001100;
console.log((a & b).toString(2));   // AND
console.log((a | b).toString(2));   // OR
console.log((a ^ b).toString(2));   // XOR
console.log((~a >>> 0).toString(2)); // NOT (unsigned)
console.log((a << 2).toString(2));  // Left shift

// XOR bytes (Uint8Array)
function xorBuffers(a, b) {
    return a.map((byte, i) => byte ^ b[i]);
}
```

### Go
```go
import "fmt"

// Integer to binary
fmt.Sprintf("%08b", 214)  // "11010110"

// Bitwise ops
a := 0b10101010
b := 0b11001100
fmt.Printf("%08b\n", a&b)   // AND
fmt.Printf("%08b\n", a|b)   // OR
fmt.Printf("%08b\n", a^b)   // XOR
fmt.Printf("%08b\n", ^a)    // NOT
fmt.Printf("%08b\n", a<<2)  // Left shift

// Bit rotation (used in SHA-256)
func rotateRight(x uint32, n uint) uint32 {
    return (x >> n) | (x << (32 - n))
}
```

---

## Binary Representations of Numbers

### Unsigned vs Signed (Two's Complement)
```
8-bit:
Unsigned: 0 to 255
Signed:  -128 to 127

11111111 = 255 (unsigned) = -1 (signed, two's complement)
10000000 = 128 (unsigned) = -128 (signed)
01111111 = 127 (both)
```

### Two's Complement (How Negative Numbers Work)
```
To negate: flip all bits, add 1
 5 = 00000101
-5 = 11111010 + 1 = 11111011

Verify: 5 + (-5) = 00000101 + 11111011 = 100000000 → 0 (overflow discarded) ✓
```

---

## Best Practices
- Use `format(n, '08b')` in Python for padded binary output
- Use XOR (`^`) for bit toggling and stream cipher operations
- Use AND (`&`) with masks for extracting specific bits
- Understand **endianness** (big-endian vs little-endian) for multi-byte values
- In security code, use **unsigned right shift** (`>>>` in Java/JS) to avoid sign extension bugs
