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
    _, phi = big_multiply_dec(p_decrement, False, q_decrement, False)

    # choose e with gcd(e, phi) = 1
    # UNCOMMENT THIS LINE FOR A RANDOM COPRIME PUBLIC KEY
    # e = random_coprime(phi)
    e = 65537

    # extended Euclid: e*x + phi*y = gcd(e, phi) = 1
    g, neg_g, x, neg_x, y, _ = big_ext_euclid_recursive(e, False, phi, False)

    # check gcd(e, phi) == 1
    if not (neg_g == False and g == 1):
        raise ValueError("random_coprime failed: gcd(e, phi) != 1")

    # |x| mod phi
    _, _, r = big_divide(abs(x), False, phi, False)

    # If x >= 0  → d = r
    # If x < 0   → d = (phi - r) mod phi
    if not neg_x:
        d = r
    else:
        if r == 0:
            d = 0
        else:
            _, d = big_substract(phi, False, r, False)

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
    message_int = int(message)
    return pow_mod(message_int, e, n)

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
        print("RSA CRYPTOSYSTEM (Built-in Arithmetic Implementation)\n")
        print("FOR DIGITAL SIGNATURE, COMMENT THE LAST PRESENTATION CALL FOR PRETTY DISPLAY")
    # safe primes generated with CLI tools
    _, p = get_number(file_p)
    _, q = get_number(file_q)

    if presentation:
        print("Primes were generated with the command openssl prime -generate -bits 1024 -safe")
        print("Using Python built-in arithmetic - significantly faster than custom implementation")
        print("Secret information:")
        print("p = " + str(p))
        print("q = " + str(q))

    # d is secret
    n, e, d = RSA_init(p, q)
    if not presentation:
        return n, e, d

    if presentation:
        print("d = " + str(d))
        print("Public key:")
        print(str(e))
        message = input("Enter the plaintext message (< 128 chars alphanumeric) to be encrypted with RSA: ")
    else:
        message = message_param
    message = convert_plaintext_to_number(message)
    encrypted_message = RSA_encrypt(str(message), e, n)
    if presentation:
        print("Plaintext to number: " + str(message))
        print("Encrypted message using ck:")
        print(str(encrypted_message))
        print("Decrypted message using dk:")
    decrypted_message = RSA_decrypt(encrypted_message, d, n)
    decrypted_message_no = str(decrypted_message)
    if presentation:
        print(convert_number_to_plaintext(int(decrypted_message_no)))

# For digital signature, this line should be commented since it stands just as a presentation
if __name__ == "__main__":
    RSA_crypto_system(True, "", "../tests/big_prime1", "../tests/big_prime2")
