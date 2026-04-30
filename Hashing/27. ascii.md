# ASCII

## What is ASCII?
**ASCII** (American Standard Code for Information Interchange) is a 7-bit character encoding standard that maps 128 characters to integers 0–127. Developed in the 1960s, it forms the foundation of all modern text encoding.

---

## ASCII Table

### Control Characters (0–31)
| Dec | Hex | Symbol | Name |
|-----|-----|--------|------|
| 0  | 00 | NUL | Null |
| 7  | 07 | BEL | Bell |
| 8  | 08 | BS  | Backspace |
| 9  | 09 | HT  | Horizontal Tab |
| 10 | 0A | LF  | Line Feed (newline) |
| 13 | 0D | CR  | Carriage Return |
| 27 | 1B | ESC | Escape |
| 32 | 20 | SP  | Space |

### Printable Characters (32–127)
```
Dec  Hex  Char    Dec  Hex  Char    Dec  Hex  Char
 32  20   (space)  64  40    @       96  60    `
 33  21    !       65  41    A       97  61    a
 34  22    "       66  42    B       98  62    b
 35  23    #       67  43    C       99  63    c
 36  24    $       68  44    D      100  64    d
 37  25    %       69  45    E      101  65    e
 38  26    &       70  46    F      102  66    f
 39  27    '       71  47    G      103  67    g
 40  28    (       72  48    H      104  68    h
 41  29    )       73  49    I      105  69    i
 42  2A    *       74  4A    J      106  6A    j
 43  2B    +       75  4B    K      107  6B    k
 44  2C    ,       76  4C    L      108  6C    l
 45  2D    -       77  4D    M      109  6D    m
 46  2E    .       78  4E    N      110  6E    n
 47  2F    /       79  4F    O      111  6F    o
 48  30    0       80  50    P      112  70    p
 49  31    1       81  51    Q      113  71    q
 50  32    2       82  52    R      114  72    r
 51  33    3       83  53    S      115  73    s
 52  34    4       84  54    T      116  74    t
 53  35    5       85  55    U      117  75    u
 54  36    6       86  56    V      118  76    v
 55  37    7       87  57    W      119  77    w
 56  38    8       88  58    X      120  78    x
 57  39    9       89  59    Y      121  79    y
 58  3A    :       90  5A    Z      122  7A    z
 59  3B    ;       91  5B    [      123  7B    {
 60  3C    <       92  5C    \      124  7C    |
 61  3D    =       93  5D    ]      125  7D    }
 62  3E    >       94  5E    ^      126  7E    ~
 63  3F    ?       95  5F    _      127  7F   DEL
```

---

## Key Ranges (Memorize These)

```
0–31   → Control characters
32     → Space
48–57  → '0' to '9' (digits)
65–90  → 'A' to 'Z' (uppercase)
97–122 → 'a' to 'z' (lowercase)
127    → DEL
```

### Useful Relationships
```
'A' = 65  →  'a' = 97  →  difference = 32 = 0x20
To convert uppercase to lowercase: char | 0x20
To convert lowercase to uppercase: char & ~0x20
'0' = 48  →  digit value = char - 48
```

---

## ASCII in Cryptography

### Why ASCII Matters
- Hash inputs are usually ASCII strings
- Passwords are ASCII (or UTF-8) encoded before hashing
- Hex encoding produces ASCII output
- Base64 output is ASCII
- PEM keys are ASCII-armored

### ASCII vs Binary in Crypto Operations
```python
# Passwords must be encoded to bytes before hashing
password = "hunter2"
password_bytes = password.encode('ascii')  # or 'utf-8'
# → b'hunter2' → bytes that can be hashed
```

---

## Implementation Examples

### Python
```python
# Char to ASCII value
ord('A')      # 65
ord('a')      # 97
ord('0')      # 48

# ASCII value to char
chr(65)       # 'A'
chr(97)       # 'a'

# Check if printable ASCII
def is_printable_ascii(s: str) -> bool:
    return all(32 <= ord(c) <= 126 for c in s)

# Encode string to ASCII bytes
"Hello".encode('ascii')    # b'Hello'
b'Hello'.decode('ascii')   # 'Hello'

# ASCII manipulation
char = 'A'
lower = chr(ord(char) | 0x20)   # 'a'
upper = chr(ord(char) & ~0x20)  # 'A'

# Caesar cipher (simple ASCII manipulation)
def caesar(text: str, shift: int) -> str:
    result = []
    for c in text:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)
```

### JavaScript
```javascript
// Char to ASCII
'A'.charCodeAt(0);    // 65
'a'.charCodeAt(0);    // 97

// ASCII to char
String.fromCharCode(65);   // 'A'
String.fromCharCode(97);   // 'a'

// Check printable ASCII
const isPrintable = str => [...str].every(c => c.charCodeAt(0) >= 32 && c.charCodeAt(0) <= 126);

// Encode to bytes (TextEncoder uses UTF-8, superset of ASCII)
const encoder = new TextEncoder();
const bytes = encoder.encode("Hello"); // Uint8Array [72, 101, 108, 108, 111]
```

---

## ASCII vs Unicode vs UTF-8

| Property | ASCII | Latin-1 | UTF-8 | UTF-16 |
|----------|-------|---------|-------|--------|
| Code points | 128 | 256 | 1,114,112 | 1,114,112 |
| Bits per char | 7 | 8 | 8–32 | 16–32 |
| English compatible | ✅ | ✅ | ✅ | ✅ |
| Emoji | ❌ | ❌ | ✅ | ✅ |
| Backwards compatible | — | ✅ ASCII | ✅ ASCII | ❌ |
| Null bytes | No | No | No (for ASCII) | Yes |

---

## Security Considerations

### SQL Injection via ASCII Encoding
```sql
-- Attacker uses ASCII/char() to bypass filters
SELECT * FROM users WHERE name = CHAR(39) -- single quote '
```

### Null Byte Injection
```
ASCII 0x00 (null byte) can truncate strings in C-based systems
file.php%00.jpg → interpreted as file.php in some systems
```

### Homoglyph Attacks (Unicode vs ASCII)
```
'a' (ASCII 97) vs 'а' (Cyrillic а, U+0430)
Visually identical, different bytes — used in phishing
```

---

## Best Practices
- Always **specify encoding explicitly** when converting strings to bytes
- Use **UTF-8** (superset of ASCII) for modern applications
- Validate input for **unexpected control characters** (0x00–0x1F)
- Be aware of **null byte injection** in security-sensitive contexts
- When comparing strings in crypto, compare **bytes not characters**
