# Copyright 2025 -Toma Dumitrescu
from helpers import *

def RSA_init(p: deque, q: deque):
    """
    Sets up the cryptosystem: calculates n, phi, e, d common parameters of RSA algorithm
    using my symbolic arithmetic tools

    Word-RAM complexities: consider p, q the effective numbers (deque digits joined)
    - Time: O(logmax(p, q) ^ 2)
    - Space: O(logmax(p, q))
    Real-RAM complexities: consider p, q the effective numbers (deque digits joined)
    - Time: O(logmax((p - 1) * (q - 1), e))
    - Space: O(1)

    :param p: safe prime p generated with openssl
    :type p: deque
    :param q: safe prime q generated with openss
    :type q: deque
    """
    # n = p * q
    _, n = big_multiply_dec(deque(p), False, deque(q), False)

    # phi = (p-1)*(q-1)
    _, p_decrement = big_substract(deque(p), False, deque([1]), False)
    _, q_decrement = big_substract(deque(q), False, deque([1]), False)
    _, phi = big_multiply_dec(deque(p_decrement), False, deque(q_decrement), False)

    # choose e with gcd(e, phi) = 1

    # UNCOMMENT THIS LINE FOR A RANDOM COPRIME PUBLIC KEY
    # e = random_coprime(phi)
    e = deque([6, 5, 5, 3, 7])

    # _, g = big_gcd(e, False, phi, False)
    # g = normalize(g)
    # if not (len(g) == 1 and g[0] == 1):
    #     e = random_coprime(phi)

    # extended Euclid: e*x + phi*y = gcd(e, phi) = 1
    g, neg_g, x, neg_x, y, _ = big_ext_euclid_recursive(deque(e), False, deque(phi), False)

    # check gcd(e, phi) == 1
    if not (neg_g == False and len(g) == 1 and g[0] == 1):
        raise ValueError("random_coprime failed: gcd(e, phi) != 1")

    # |x| mod phi  (we treat digits of x as abs(x); sign is in neg_x)
    x_abs = strip_zeroes(deque(x))
    _, _, r = big_divide(deque(x_abs), False, deque(phi), False)   # r = |x| mod phi

    # If x >= 0  → d = r
    # If x < 0   → d = (phi - r) mod phi
    if not neg_x:
        d = r
    else:
        if is_zero(r):
            # x ≡ 0 (mod phi) would contradict gcd=1, so this is “impossible”
            # but we guard anyway
            d = deque([0])
        else:
            _, d = big_substract(deque(phi), False, deque(r), False)  # phi - r

    return n, e, d

def RSA_encrypt(message, e, n):
    """
    RSA_encrypt: transforms the numerical message (as string) in a deque and encrypts
    using M ^ e mod n symbolic arithmetic function

    Word-RAM complexities: consider e, message, n the effective numbers (deque digits joined)
    - Time:  O(log2(e) * (logmax(message, e) ^ (log2(3)) + logmax(message, n) ^ 2))
    - Space: O(logmax(message, e))
    Real-RAM complexities: consider e, message, n the effective numbers (deque digits joined)
    - Time: O(log(e))
    - Space: O(1)

    :param message: numerical message as string (coverted from plaintext)
    :param e: public encryption key as deque
    :param n: classic n RSA as deque
    """
    message_deque = deque()
    for c in message:
        message_deque.append(int(c))
    return pow_mod(message_deque, e, deque(n))

def RSA_decrypt(enc_message, d, n):
    """
    RSA_decrypt: transforms encrypted_message C into the original numerical message
    using C ^ d mod n with symbolic arithmetic function pow_mod

    Word-RAM complexities: consider enc_message, d, n the effective numbers (deque digits joined)
    - Time:  O(log2(d) * (logmax(enc_message, d) ^ (log2(3)) + logmax(enc_message, n) ^ 2))
    - Space: O(logmax(enc_message, d))
    Real-RAM complexities: consider enc_message, d, n the effective numbers (deque digits joined)
    - Time: O(log(d))
    - Space: O(1)

    :param enc_message: encrypted numerical message as a deque
    :param d: decryption key as deque
    :param n: RSA n as deque
    """
    return pow_mod(enc_message, d, n)

def RSA_crypto_system(presentation: bool, message_param: str, file_p: str, file_q: str):
    if presentation:
        print("RSA CRYPTOSYSTEM\n")
        print("FOR DIGITAL SIGNATURE, COMMENT THE LAST PRESENTATION CALL FOR PRETTY DISPLAY")
    # safe primes generated with CLI tools
    _, p = get_number(file_p)
    _, q = get_number(file_q)

    if presentation:
        print("Primes were generated with the command openssl prime -generate -bits 512 -safe")
        print("For modern standards 2048 bits, there should be optimizations for the decryption such as Chinese Reminder Theorem")
        print("For 0 - 300 bits, the decryption runs in 0-6s, for 512 bits 30 - 40s")
        print("Secret information:")
        print("p = " + ''.join(map(str, p)))
        print("q = " + ''.join(map(str, q)))

    # d is secret
    n, e, d = RSA_init(p, q)
    if not presentation:
        return n, e, d

    if presentation:
        print("d = " + ''.join(map(str, d)))
        print("Public key:")
        print(''.join(map(str, e)))
        message = input("Enter the plaintext message (< 128 chars alphanumeric) to be encrypted with RSA: ")
    else:
        message = message_param
    message = convert_plaintext_to_number(message)
    encrypted_message = RSA_encrypt(str(message), e, n)
    if presentation:
        print("Plaintext to number: " + str(message))
        print("Encrypted message using ck:")
        print(''.join(map(str, encrypted_message)))
        print("Decrypted message using dk:")
    decrypted_message = RSA_decrypt(encrypted_message, d, n)
    decrypted_message_no = ''.join(map(str, decrypted_message))
    if presentation:
        print(convert_number_to_plaintext(int(decrypted_message_no)))

# For digital signature, this line should be commented since it stands just as a presentation
if __name__ == "__main__":
    RSA_crypto_system(True, "", "../data/rsa_p_prime", "../data/rsa_q_prime")
