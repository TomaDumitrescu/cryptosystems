from collections import deque
import random
import math

# ============================================================================
# CONVERSION UTILITIES
# ============================================================================

def deque_to_int(d, negative=False):
    """Convert a deque of digits to a Python integer."""
    if len(d) == 0:
        return 0
    num = int(''.join(map(str, d)))
    return -num if negative else num

# ============================================================================
# BASIC OPERATIONS - Return ints directly
# ============================================================================

def compare(a, b):
    """Compare two numbers (deque or int). Returns 1, -1, or 0."""
    num_a = deque_to_int(a) if isinstance(a, deque) else a
    num_b = deque_to_int(b) if isinstance(b, deque) else b
    return (num_a > num_b) - (num_a < num_b)

def strip_zeroes(x):
    """For compatibility - converts deque to int."""
    return deque_to_int(x) if isinstance(x, deque) else x

def is_zero(x):
    """Check if number is zero."""
    num = deque_to_int(x) if isinstance(x, deque) else x
    return num == 0

def get_number(filename):
    """Read a big number from file. Returns (negative, int_value)."""
    big_number = deque()
    negative = False
    with open(filename, 'r') as f:
        while True:
            c = f.read(1)
            if not c:
                break
            if c == '-':
                negative = True
                continue
            if '0' <= c <= '9':
                big_number.append(ord(c) - ord('0'))
    return negative, big_number

def big_add(a, negative_a, b, negative_b):
    """Addition using Python built-in. Returns (negative_result, int_result)."""
    num_a = deque_to_int(a, negative_a) if isinstance(a, deque) else (a if not negative_a else -a)
    num_b = deque_to_int(b, negative_b) if isinstance(b, deque) else (b if not negative_b else -b)
    result = num_a + num_b
    return result < 0, abs(result)

def big_substract(a, negative_a, b, negative_b):
    """Subtraction using Python built-in. Returns (negative_result, int_result)."""
    num_a = deque_to_int(a, negative_a) if isinstance(a, deque) else (a if not negative_a else -a)
    num_b = deque_to_int(b, negative_b) if isinstance(b, deque) else (b if not negative_b else -b)
    result = num_a - num_b
    return result < 0, abs(result)

    r = 0
    while a and b:
        sub = a.pop() - b.pop() - r
        if sub < 0:
            r = 1
            sub += 10
        else:
            r = 0
        c.appendleft(sub)

    while a:
        sub = a.pop() - r
        if sub < 0:
            r = 1
            sub += 10
        else:
            r = 0
        c.appendleft(sub)

    return negative_c, strip_zeroes(c)

def big_multiply_dec(A, neg_a, B, neg_b):
    """Multiplication using Python built-in. Returns (negative_result, int_result)."""
    num_a = deque_to_int(A, neg_a) if isinstance(A, deque) else (A if not neg_a else -A)
    num_b = deque_to_int(B, neg_b) if isinstance(B, deque) else (B if not neg_b else -B)
    result = num_a * num_b
    return result < 0, abs(result)

def div2_dec(a):
    """Compute floor(a / 2). Returns int."""
    num = deque_to_int(a) if isinstance(a, deque) else a
    return num // 2

def mod_big(a, b):
    """Compute a mod b. Returns int."""
    num_a = deque_to_int(a) if isinstance(a, deque) else a
    num_b = deque_to_int(b) if isinstance(b, deque) else b
    if num_b == 0:
        raise ZeroDivisionError("modulo by zero")
    return num_a % num_b

def pow_mod(a, b, n):
    """Compute (a ** b) mod n using Python built-in pow. Returns int."""
    num_a = deque_to_int(a) if isinstance(a, deque) else a
    num_b = deque_to_int(b) if isinstance(b, deque) else b
    num_n = deque_to_int(n) if isinstance(n, deque) else n
    return pow(num_a, num_b, num_n)


def big_divide(A, neg_a, B, neg_b):
    """Integer division using Python built-in. Returns (q_negative, quotient_int, remainder_int)."""
    num_a = deque_to_int(A, neg_a) if isinstance(A, deque) else (A if not neg_a else -A)
    num_b = deque_to_int(B, neg_b) if isinstance(B, deque) else (B if not neg_b else -B)
    if num_b == 0:
        raise ZeroDivisionError("division by zero")
    quotient = abs(num_a) // abs(num_b)
    remainder = abs(num_a) % abs(num_b)
    q_negative = neg_a ^ neg_b
    if quotient == 0:
        q_negative = False
    return q_negative, quotient, remainder

def big_gcd(A, neg_a, B, neg_b):
    """GCD using Python built-in. Returns (negative, int_result)."""
    num_a = abs(deque_to_int(A, neg_a) if isinstance(A, deque) else A)
    num_b = abs(deque_to_int(B, neg_b) if isinstance(B, deque) else B)
    result = math.gcd(num_a, num_b)
    return (False, result)

def big_ext_euclid_recursive(a, neg_a, b, neg_b):
    """Extended Euclidean Algorithm. Returns (d, neg_d, x, neg_x, y, neg_y) where values are ints."""
    num_a = deque_to_int(a, neg_a) if isinstance(a, deque) else (a if not neg_a else -a)
    num_b = deque_to_int(b, neg_b) if isinstance(b, deque) else (b if not neg_b else -b)
    
    def ext_gcd(a, b):
        if b == 0:
            return a, 1, 0
        gcd, x1, y1 = ext_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y
    
    gcd, x, y = ext_gcd(num_a, num_b)
    return (abs(gcd), gcd < 0, abs(x), x < 0, abs(y), y < 0)

def random_less_than(lim):
    """Generate random in [1, lim). Returns int."""
    num_lim = deque_to_int(lim) if isinstance(lim, deque) else lim
    if num_lim <= 1:
        raise ValueError("Limit must be greater than 1")
    r = random.randint(1, num_lim - 1)
    while r == 1:
        r = random.randint(1, num_lim - 1)
    return r

def random_coprime(lim):
    """Generate random coprime with lim. Returns int."""
    num_lim = deque_to_int(lim) if isinstance(lim, deque) else lim
    while True:
        x = random_less_than(lim)
        if x <= 1:
            continue
        if math.gcd(x, num_lim) == 1:
            return x

def convert_plaintext_to_number(plaintext):
    return int.from_bytes(plaintext.encode('utf-8'), byteorder='big')

def convert_number_to_plaintext(msg_number):
    return msg_number.to_bytes((msg_number.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

def get_code(filename):
    with open(filename, 'r') as f:
        return list(map(str.strip, f.readlines()))
    return []