from collections import deque
import random

def compare(a: deque, b: deque) -> int:
    """
    Compare two normalized big integers.

    Word-RAM complexities:
    - Time: O(max(len(a), len(b)))
    - Space: O(1)
    Real-RAM complexities:
    - Time: O(max(len(a), len(b)))
    - Space: O(1)

    Returns:
      1  if a > b
     -1  if a < b
      0  if a == b
    """
    len_a = len(a)
    len_b = len(b)
    if len_a != len_b:
        return 1 if len_a > len_b else -1

    ba = bytes(a)
    bb = bytes(b)

    return (ba > bb) - (ba < bb)

def strip_zeroes(x: deque) -> deque:
    """
    Remove leading zeros from a number (in-place).
    
    Word-RAM complexities:
    - Time: O(len(x))
    - Space: O(1)
    Real-RAM complexities:
    - Time: O(len(x))
    - Space: O(1)
    """
    while len(x) > 1 and x[0] == 0:
        x.popleft()
    return x

def is_zero(x: deque) -> bool:
    """
    Verifies if a number is zero.

    Word-RAM complexities:
    - Time: O(1)
    - Space: O(1)
    Real-RAM complexities:
    - Time: O(1)
    - Space: O(1)
    """
    return len(x) == 1 and x[0] == 0

def get_number(filename):
    """
    Read a big number from a file.

    Word-RAM complexities:
    - Time: O(len(filename))
    - Space: O(len(filename))
    Real-RAM complexities:
    - Time: O(len(filename))
    - Space: O(len(filename))
    """
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
    """
    Addition of two big numbers stored as deques. Parameters should be copies of the actual numbers to avoid destroying them.

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log max(a, b))
    - Space: log max(a, b)
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    """
    negative_c = False
    c = deque()

    if negative_a == True and negative_b == True:
        negative_c = True
    elif negative_a == True and negative_b == False:
        return big_substract(b, False, a, False)
    elif negative_a == False and negative_b == True:
        return big_substract(a, False, b, False)

    # Decimal addition with carry
    r = 0
    while a and b:
        add = a.pop() + b.pop() + r
        r = add // 10
        c.appendleft(add % 10)

    while a:
        add = a.pop() + r
        r = add // 10
        c.appendleft(add % 10)

    while b:
        add = b.pop() + r
        r = add // 10
        c.appendleft(add % 10)

    if r != 0:
        c.appendleft(r)

    return negative_c, c

def big_substract(a, negative_a, b, negative_b):
    """
    Subtraction of two big numbers with sign handling. Parameters should be copies to avoid alteration.

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log max(a, b))
    - Space: log max(a, b)
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    """

    negative_c = False
    c = deque()

    if negative_a == True and negative_b == True:
        return big_substract(b, False, a, False)
    elif negative_a == True and negative_b == False:
        return big_add(a, True, b, True)
    elif negative_a == False and negative_b == True:
        return big_add(a, False, b, False)

    s = compare(a, b)
    if s == -1:
        negative_c, c = big_substract(b, negative_b, a, negative_a)
        return not negative_c, c

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

def big_multiply_dec(A: deque, neg_a: bool, B: deque, neg_b: bool):
    """
    Karatsuba multiplication on decimal digits with sign handling.
    Uses a schoolbook O(n^2) method for small n (faster in Python).

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(logmax(a, b) ^ (log2(3)))
    - Space: O(logmax(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    """
    neg_result = neg_a ^ neg_b

    if len(A) == 1 and A[0] == 0:
        return False, deque([0])
    if len(B) == 1 and B[0] == 0:
        return False, deque([0])

    n = max(len(A), len(B))

    if n <= 32:
        # pad to same length (not strictly necessary but convenient)
        while len(A) < len(B):
            A.appendleft(0)
        while len(B) < len(A):
            B.appendleft(0)

        a_digits = list(A)
        b_digits = list(B)
        m = len(a_digits)
        # result has at most 2m digits
        res = [0] * (2 * m)

        # classic O(n^2) multiply, LSD at right
        for i in range(m - 1, -1, -1):
            carry = 0
            for j in range(m - 1, -1, -1):
                idx = i + j + 1
                tmp = res[idx] + a_digits[i] * b_digits[j] + carry
                res[idx] = tmp % 10
                carry = tmp // 10
            res[i] += carry

        result = deque(res)
        strip_zeroes(result)
        return neg_result, result

    # Pad to equal even length
    while len(A) < n:
        A.appendleft(0)
    while len(B) < n:
        B.appendleft(0)
    if n % 2 == 1:
        n += 1
        A.appendleft(0)
        B.appendleft(0)

    m = n // 2
    list_A = list(A)
    list_B = list(B)
    a1 = deque(list_A[:m])
    a0 = deque(list_A[m:])
    b1 = deque(list_B[:m])
    b0 = deque(list_B[m:])

    # Karatsuba recursion
    _, z2 = big_multiply_dec(deque(a1), False, deque(b1), False)
    _, z0 = big_multiply_dec(deque(a0), False, deque(b0), False)

    _, a_sum = big_add(a1, False, a0, False)
    _, b_sum = big_add(b1, False, b0, False)
    _, z1 = big_multiply_dec(a_sum, False, b_sum, False)

    _, z1 = big_substract(z1, False, deque(z2), False)
    _, z1 = big_substract(z1, False, deque(z0), False)

    # Shift and combine
    z2.extend([0]*(2*m))
    z1.extend([0]*m)

    _, tmp = big_add(z2, False, z1, False)
    _, result = big_add(tmp, False, z0, False)

    return neg_result, strip_zeroes(result)

def div2_dec(a: deque) -> deque:
    """
    Compute floor(a / 2) for a non-negative big integer represented
    as a deque of decimal digits (MSD first).

    Uses only digit-level arithmetic (O(n)), plus normalize.
    Does NOT use big_divide.
    """

    if len(a) == 1 and a[0] == 0:
        return deque([0])

    carry = 0
    q = deque()

    for d in a:
        # d is a single decimal digit 0..9
        cur = carry * 10 + d      # carry is 0 or 1, so cur in [0..19]
        q_digit = cur // 2        # integer division by 2 on small int
        carry = cur % 2           # remainder 0 or 1
        q.append(q_digit)

    return strip_zeroes(q)

def mod_big(a: deque, b: deque) -> deque:
    """
    Compute a mod b for non-negative big integers (decimal digits, MSD first).
    Uses big_divide (long division), so it's O(len(a) * len(b)) but with
    much smaller constants than the repeated-subtraction version.

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(logmax(a, b) ^ 2)
    - Space: O(logmax(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    """

    if is_zero(b):
        raise ZeroDivisionError("modulo by zero")

    if compare(a, b) < 0:
        return a

    _, _, r = big_divide(a, False, b, False)
    return r

def pow_mod(a, b, n):
    """
    Compute (a ** b) mod n using binary exponentiation on big-int deques.
    a, b, n are deques of decimal digits (MSD first).

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log2(b) * (logmax(a, b) ^ (log2(3)) + logmax(a, n) ^ 2))
    - Space: O(logmax(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    """
    ONE = deque([1])

    # Reduce base: a = a mod n
    a = mod_big(a, n)
    result = deque(ONE)

    # While b > 0
    while not is_zero(b):
        # If exponent is odd (check last decimal digit)
        if b[-1] % 2 == 1:
            # result = (result * a) mod n
            _, prod = big_multiply_dec(result, False, deque(a), False)
            result = mod_big(prod, n)

        # a = (a * a) mod n
        _, sq = big_multiply_dec(a, False, deque(a), False)
        a = mod_big(sq, n)

        # b = floor(b / 2)
        b = div2_dec(b)

    return strip_zeroes(result)

def big_divide(A, neg_a, B, neg_b):
    """
    Integer division on big numbers (base-10 deques, MSB left).
    Returns (q_negative, quotient_digits, remainder_digits)
    satisfying: a = b * q + r, with 0 <= r < |b|. In addition to the naive model, it
    uses binary search to search for the digit d that multiplied with the divider gives
    what is expected to the left.

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(logmax(a, b) ^ 2)
    - Space: O(logmax(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)

    Uses only:
      - compare
      - strip_zeroes
      - big_substract
      - is_zero
    """

    # division by zero
    if len(B) == 1 and B[0] == 0:
        raise ZeroDivisionError("division by zero")

    # Absolute-value division; handle signs at the end
    orig_neg_a, orig_neg_b = neg_a, neg_b

    # If |A| < |B|, quotient = 0, remainder = |A|
    if compare(A, B) < 0:
        q = deque([0])
        r = deque(A)
        q_negative = orig_neg_a ^ orig_neg_b
        if is_zero(q):
            q_negative = False
        return q_negative, q, r

    quotient = deque()
    remainder = deque()

    mul_cache = [deque([0]), deque(B)]
    for i in range(2, 11):
        _, result = big_add(deque(mul_cache[i - 1]), False, deque(B), False)
        mul_cache.append(result)

    # Long division in base 10
    for digit in A:
        # remainder = remainder * 10 + digit
        remainder.append(digit)
        strip_zeroes(remainder)

        # If remainder < B, quotient digit is 0
        if compare(remainder, B) < 0:
            quotient.append(0)
            continue

        # Find q_digit in [0..9] such that q_digit * B <= remainder < (q_digit+1) * B
        q_digit = 0
        low = 0
        high = 9
        while low <= high:
            mid = (low + high) // 2
            if compare(remainder, mul_cache[mid]) >= 0:
                if compare(remainder, mul_cache[mid + 1]) < 0:
                    q_digit = mid
                low = mid + 1
            else:
                high = mid - 1

        _, remainder = big_substract(remainder, False, deque(mul_cache[q_digit]), False)

        quotient.append(q_digit)

    # Set quotient sign; remainder is always non-negative and < |B|
    q_negative = orig_neg_a ^ orig_neg_b
    if is_zero(quotient):
        q_negative = False

    return q_negative, strip_zeroes(quotient), strip_zeroes(remainder)

def big_gcd(A: deque, neg_a: bool, B: deque, neg_b: bool):
    """
    Euclidean GCD for big integers.

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log b * logmax(a, b) ^ 2)
    - Space: O(log max(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log(max(a, b)))
    - Space: O(1)
    """

    if is_zero(A) and is_zero(B):
        return (False, deque([0]))
    if is_zero(A):
        return (False, deque(B))
    if is_zero(B):
        return (False, deque(A))

    while not is_zero(B):
        _, _, R = big_divide(deque(A), False, deque(B), False)
        A, B = B, R
    
    strip_zeroes(A)
    return (False, A)

def big_ext_euclid_recursive(a: deque, neg_a: bool, b: deque, neg_b: bool):
    """
    Computes the Extended Euclidean Algorithm recursively for arbitrary-precision
    integers represented as digit deques with explicit sign flags. It finds gcd(a,b)
    and integers x, y such that: a·x + b·y = gcd(a,b).

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log b * logmax(a, b) ^ 2)
    - Space: O(log max(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(log(max(a, b)))
    - Space: O(1)

    Parameters
    ----------
    a : deque
        Non-negative integer represented as a deque of digits (base 10).
    neg_a : bool
        True if 'a' is negative, False otherwise.
    b : deque
        Non-negative integer represented as a deque of digits (base 10).
    neg_b : bool
        True if 'b' is negative, False otherwise.

    Returns
    -------
    (d, neg_d, x, neg_x, y, neg_y) : tuple

    Word-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(logmax(a, b) ^ 2)
    - Space: O(logmax(a, b))
    Real-RAM complexities: consider a, b the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    """
    zero = deque([0])

    # Base case
    if b == zero:
        # gcd = a, x = 1, y = 0
        return (a, neg_a, deque([1]), False, deque([0]), False)

    # a = q * b + r
    q_negative, q, r = big_divide(a, neg_a, deque(b), neg_b)

    # Recursive call
    d, neg_d, x1, neg_x1, y1, neg_y1 = big_ext_euclid_recursive(b, neg_b, r, False)

    # x = y1
    x, neg_x = y1, neg_y1

    # qy1 = q * y1
    neg_qy1, qy1 = big_multiply_dec(q, q_negative, y1, neg_y1)

    # y = x1 - qy1
    neg_y, y = big_substract(x1, neg_x1, qy1, neg_qy1)

    return (d, neg_d, x, neg_x, y, neg_y)

def random_less_than(lim):
    """
    It generates a random number in the interval [1, lim). At cryptographic algorithms, it should
    be sanitized so that 1 is not used because it can lead to different attacks.

    Word-RAM complexities: consider n (lim) the effective numbers (deque digits joined)
    - Time: ~~~ log(n) * number_of-tries ~~~ O(log(n) * (99...9 with log(n) digits - log(n))
    - Space: O(log n)
    Real-RAM complexities: consider n the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    :param lim: strictly upper bound integer in the form of a deque
    """
    n = len(lim)
    while True:
        r = strip_zeroes(deque(random.randint(0, 9) for _ in range(n)))
        if compare(r, lim) < 0 and compare(r, deque([1])) != 0:
            return r

def random_coprime(lim):
    """
    It generates a random coprime with lim.

    Word-RAM complexities: consider n the effective numbers (deque digits joined)
    - Time: ~~~ log(n) ^ 2 * number_of-tries ~~~ O(log(n) ^ 2 * (100.000 with log(n) 0-digits - phi(n))
    - Space: O(log n)
    Real-RAM complexities: consider n the effective numbers (deque digits joined)
    - Time: O(1)
    - Space: O(1)
    :param lim: strictly upper bound integer in the form of a deque
    """
    one = deque([int(1)])
    while True:
        x = random_less_than(lim)
        if compare(x, one) <= 0:
            continue

        _, c = big_gcd(x, False, lim, False)
        if compare(c, one) == 0:
            return strip_zeroes(x)

# Since messages are always sent in small chunks, no need for symbolic arithmetic here
def convert_plaintext_to_number(plaintext: str):
    return int.from_bytes(plaintext.encode('utf-8'), byteorder='big')

def convert_number_to_plaintext(msg_number: int):
    return msg_number.to_bytes((msg_number.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

# Huffman trees tools
def get_code(filename):
    with open(filename, 'r') as f:
        return list(map(str.strip, f.readlines()))

    return []