# Hexadecimal (Hex) Encoding

## What is Hex?
**Hexadecimal** is a base-16 number system using digits `0–9` and letters `A–F` (case-insensitive). It is widely used in cryptography and computing to represent binary data in a human-readable format.

```
Base-2  (Binary):      11111111
Base-10 (Decimal):     255
Base-16 (Hex):         FF
```

---

## Hex Alphabet

| Decimal | Hex | Binary |
|---------|-----|--------|
| 0  | 0 | 0000 |
| 1  | 1 | 0001 |
| 2  | 2 | 0010 |
| 3  | 3 | 0011 |
| 4  | 4 | 0100 |
| 5  | 5 | 0101 |
| 6  | 6 | 0110 |
| 7  | 7 | 0111 |
| 8  | 8 | 1000 |
| 9  | 9 | 1001 |
| 10 | A | 1010 |
| 11 | B | 1011 |
| 12 | C | 1100 |
| 13 | D | 1101 |
| 14 | E | 1110 |
| 15 | F | 1111 |

---

## How Hex Encoding Works

Each byte (8 bits) maps to **exactly 2 hex characters**:
```
Byte:  0x4A  =  0100 1010
Hex:   4     A
       ↑     ↑
    upper   lower
    nibble  nibble
```

### Example: "Hello" in Hex
```
H  →  72  →  48
e  →  101 →  65
l  →  108 →  6C
l  →  108 →  6C
o  →  111 →  6F

"Hello" = 48 65 6C 6C 6F
```

---

## Hex in Cryptography
- **Hash outputs**: MD5 = 32 hex chars, SHA-256 = 64 hex chars, SHA-512 = 128 hex chars
- **Keys**: AES-256 key = 64 hex chars (32 bytes)
- **Nonces/IVs**: displayed as hex
- **Memory addresses**: shown in hex (0x7fff5fc...)
- **Color codes in web**: #FF5733

---

## Implementation Examples

### Python
```python
# Bytes to hex
data = b"Hello"
hex_str = data.hex()
print(hex_str)  # 48656c6c6f

# With spaces (visual grouping)
hex_spaced = ' '.join(f'{b:02x}' for b in data)
print(hex_spaced)  # 48 65 6c 6c 6f

# Hex to bytes
decoded = bytes.fromhex("48656c6c6f")
print(decoded)  # b'Hello'

# Using binascii
import binascii
hex_str = binascii.hexlify(b"Hello").decode()
original = binascii.unhexlify(hex_str)

# Integer to hex
print(hex(255))     # '0xff'
print(f"{255:02x}") # 'ff'
print(f"{255:08x}") # '000000ff' (padded to 8 chars)
```

### JavaScript
```javascript
// String to hex
function strToHex(str) {
    return Array.from(str)
        .map(c => c.charCodeAt(0).toString(16).padStart(2, '0'))
        .join('');
}
console.log(strToHex("Hello")); // 48656c6c6f

// Hex to string
function hexToStr(hex) {
    return hex.match(/.{2}/g)
        .map(byte => String.fromCharCode(parseInt(byte, 16)))
        .join('');
}

// Buffer to hex (Node.js)
const buf = Buffer.from("Hello");
console.log(buf.toString('hex')); // 48656c6c6f

// Hex to Buffer
const restored = Buffer.from("48656c6c6f", 'hex');
```

### Go
```go
import "encoding/hex"

// Encode
encoded := hex.EncodeToString([]byte("Hello"))
// "48656c6c6f"

// Decode
decoded, err := hex.DecodeString("48656c6c6f")
// []byte("Hello")
```

### Rust
```rust
// Using hex crate
let encoded = hex::encode(b"Hello");  // "48656c6c6f"
let decoded = hex::decode("48656c6c6f").unwrap();
```

---

## Hex vs Base64 Comparison

| Property | Hex | Base64 |
|----------|-----|--------|
| Alphabet size | 16 chars | 64 chars |
| Size expansion | 2× original | 1.33× original |
| Readability | High (each byte clear) | Lower |
| Use case | Debugging, hashes, keys | Data transfer, storage |
| Characters | 0-9, a-f | A-Z, a-z, 0-9, +, / |

---

## Size Examples

| Data | Bytes | Hex chars | Base64 chars |
|------|-------|-----------|--------------|
| MD5 hash | 16 | 32 | 24 |
| SHA-1 hash | 20 | 40 | 28 |
| SHA-256 hash | 32 | 64 | 44 |
| SHA-512 hash | 64 | 128 | 88 |
| AES-128 key | 16 | 32 | 24 |
| AES-256 key | 32 | 64 | 44 |

---

## Common Hex Prefixes

| Prefix | Language/Context |
|--------|-----------------|
| `0x` | C, Python, JavaScript, Rust |
| `#` | CSS colors |
| `\x` | Escape sequences in strings |
| `U+` | Unicode code points |
| `%` | URL encoding |

---

## Best Practices
- Use **lowercase hex** for consistency (`a-f` not `A-F`)
- Always **zero-pad** to fixed length (`02x` format)
- Use built-in library functions — don't roll your own hex encoder
- For display, add **spaces or colons** between bytes for readability: `48:65:6c:6c:6f`
- When comparing hashes, always **compare bytes** not hex strings (avoid timing attacks)
