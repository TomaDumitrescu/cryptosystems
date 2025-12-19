# CI Project 2 - Cryptography & Information Theory

## Project Structure

This project implements fundamental cryptographic protocols using **two different arithmetic approaches**:

### 📁 Folder Organization

```
CI_project2/
├── custom_arithmetic/      # Original deque-based symbolic arithmetic implementation
│   ├── helpers.py         # Custom big integer operations (Karatsuba, extended Euclid, etc.)
│   ├── rsa.py            # RSA encryption/decryption
│   ├── dh.py             # Diffie-Hellman key exchange
│   ├── el_gamal.py       # ElGamal cryptosystem
│   └── digital_sign.py   # Digital signatures
│
├── builtin_arithmetic/     # Python built-in arithmetic implementation
│   ├── helpers.py         # Wrapper converting deque ↔ int, uses Python built-ins
│   ├── rsa.py            # RSA using built-in arithmetic
│   ├── dh.py             # Diffie-Hellman using built-in arithmetic
│   ├── el_gamal.py       # ElGamal using built-in arithmetic
│   └── digital_sign.py   # Digital signatures using built-in arithmetic
│
├── data/                   # Shared data files
│   ├── *_prime files      # Pre-generated large prime numbers
│   ├── huffman_input      # Test data for Huffman coding
│   └── code_words         # Code word test data
│
├── tests/                  # Test files and additional test data
│
├── huffman_tree.py        # Huffman coding implementation (shared)
├── code_trees.py          # Additional tree structures (shared)
└── README.md              # This file
```

## 🔬 Two Implementations

### 1. **custom_arithmetic/** - Symbolic Arithmetic with Deque
- **Purpose**: Educational implementation showing algorithms from scratch
- **Data Structure**: Uses `collections.deque` to store digits (Most Significant Digit first)
- **Algorithms**: 
  - Karatsuba multiplication for O(n^1.585) complexity
  - Binary modular exponentiation
  - Extended Euclidean algorithm for modular inverses
  - Custom division with binary search optimization
- **Performance**: Slower but demonstrates algorithmic complexity analysis
- **Complexity Labels**: Includes detailed Word-RAM and Real-RAM complexity annotations
- **Returns**: Deque objects with explicit sign flags

### 2. **builtin_arithmetic/** - Python Built-in Arithmetic
- **Purpose**: Fast, production-ready implementation
- **Optimization Strategy**: 
  - Accepts deques as input (API compatibility)
  - Converts to Python `int` once on entry
  - Uses highly optimized C-based Python integer operations
  - Returns `int` directly (no conversion back to deque)
- **Key Improvement**: Eliminated expensive deque↔int round-trips
- **Complexity**: O(1) in Real-RAM model (using Python's optimized arbitrary-precision arithmetic)
- **Performance**: 64x to 12,726x faster depending on operation
- **Returns**: Python `int` objects (different from custom implementation)
- **Use Case**: Practical applications, performance benchmarking

## 🎯 Key Design Principles

### API Compatibility
Both implementations accept deques as input parameters, maintaining interface compatibility. However:
- **custom_arithmetic/**: Input deque → Output deque
- **builtin_arithmetic/**: Input deque → Output int (optimized for performance)

### Performance Optimization (builtin_arithmetic/)
The builtin implementation follows this pattern:
```python
def operation(deque_input, ...):
    # Convert once on entry
    num = deque_to_int(deque_input)
    
    # Use fast Python built-ins
    result = native_operation(num, ...)
    
    # Return int directly (no conversion back)
    return result
```

This eliminates the conversion overhead that was negating Python's performance advantages.

### Example:
```python
from custom_arithmetic import helpers as custom
from builtin_arithmetic import helpers as builtin
from collections import deque

# Both accept deques as input
a = deque([1, 2, 3])  # 123
b = deque([4, 5, 6])  # 456

# Custom returns deque
_, result_custom = custom.big_multiply_dec(a, False, b, False)
# result_custom is deque([5, 6, 0, 8, 8])  # 56088

# Builtin returns int
_, result_builtin = builtin.big_multiply_dec(a, False, b, False)
# result_builtin is 56088 (int)

# Both represent the same value
assert int(''.join(map(str, result_custom))) == result_builtin
```

## 🧪 Performance Benchmarking

Run the comparison script to see performance differences:
```bash
python compare.py
```

### Sample Results (512-bit primes, 155 digits):

| Operation | Custom (deque) | Builtin (int) | Speedup |
|-----------|----------------|---------------|---------|
| RSA Key Generation | 0.012s | 0.000s | **64x** |
| RSA Encryption | 0.446s | 0.000s | **7,307x** |
| RSA Decryption | 45.689s | 0.053s | **864x** |
| Large Modular Exp (7^50000) | 0.129s | 0.000s | **1,869x** |
| Extended Euclidean | 0.011s | 0.000s | **111x** |
| Diffie-Hellman Exchange | 25.217s | 0.002s | **12,726x** |
| ElGamal Encryption | 32.342s | 0.003s | **10,557x** |

**Key Insight**: The builtin implementation is 2-4 orders of magnitude faster while maintaining cryptographic correctness.

## 🚀 Running the Code

### Individual Cryptographic Protocols

**Custom Arithmetic (Slower, Educational):**
```bash
cd custom_arithmetic
python rsa.py           # RSA demo
python dh.py            # Diffie-Hellman demo
python el_gamal.py      # ElGamal demo
python digital_sign.py  # Digital signature demo
```

**Built-in Arithmetic (Faster, Production):**
```bash
cd builtin_arithmetic
python rsa.py           # Fast RSA demo
python dh.py            # Fast Diffie-Hellman demo
python el_gamal.py      # Fast ElGamal demo
python digital_sign.py  # Fast digital signature demo
```

### Performance Comparison
```bash
python compare.py       # Benchmark both implementations
```

The comparison script runs 1 iteration of each cryptographic operation on both implementations and displays:
- Execution time for each
- Speedup factor (how much faster builtin is)
- Result verification (confirms both produce identical cryptographic results)

## 📊 Understanding the Performance Gap

### Why is builtin_arithmetic so much faster?

1. **C Implementation**: Python's `int` type uses highly optimized C code for arithmetic
2. **No Conversion Overhead**: Eliminated expensive digit-by-digit deque↔int conversions
3. **Native Algorithms**: Karatsuba and other optimizations built into Python's integer operations
4. **Memory Efficiency**: Direct integer operations vs. managing deque objects

### When to use each implementation?

**Use custom_arithmetic/ when:**
- Learning how cryptographic algorithms work internally
- Understanding complexity analysis (Word-RAM vs Real-RAM)
- Studying big integer arithmetic implementation
- Educational/academic purposes

**Use builtin_arithmetic/ when:**
- Building actual cryptographic applications
- Performance matters
- Processing large keys (2048-bit or higher)
- Production environments

## 📚 Cryptographic Protocols Implemented

1. **RSA** - Public key encryption and decryption
2. **Diffie-Hellman** - Key exchange protocol
3. **ElGamal** - Public key encryption with broadcast capability
4. **Digital Signatures** - Message authentication using RSA

All implementations include:
- Complexity analysis (Word-RAM and Real-RAM models)
- Detailed docstrings
- Security considerations
- Test cases

## 👥 Authors
- Toma Dumitrescu
- Marina Simion