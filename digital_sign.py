from rsa import *

def sign_message(n_a, n_b, e_b, d_a, msg_fmt, message_no):
    """
    sign_message - signs the message by encrypting it with B's key and them decrypting with A's key

    Word-RAM complexities: consider n_a, n_b, e_b, d_a, msg_fmt, message_no the effective numbers (deque digits joined)
    - Time: O(logmax(e_b, d_a) * (logmax(message, enc_message, e_b, d_a) ^ (log2(3)) + logmax(message, n_a, n_b) ^ 2))
    - Space: O(log(msg_fmt))
    Real-RAM complexities: consider n_a, n_b, e_b, d_a, msg_fmt, message_no the effective numbers (deque digits joined)
    - Time: O(log(e_b) + log(d_a))
    - Space: O(log(msg_fmt))

    :param n_a: n_a as deque from Alice's RSA cryptosystem
    :param n_b: n_b as deque from Bob's RSA cryptosystem
    :param e_b: e_b as deque from Bob's RSA cryptosystem
    :param d_a: d_a as deque from Alice's RSA cryptosystem
    :param msg_fmt: the message in the number form as deque
    :param message_no: the message in the number form as string
    """
    enc_message = RSA_encrypt(deque(message_no), deque(e_b), deque(n_b))
    if n_a < n_b:
        dec_a_message = RSA_decrypt(deque(msg_fmt), deque(d_a), deque(n_a))
        signature = RSA_encrypt(''.join(map(str, dec_a_message)), deque(e_b), deque(n_b))
        return (enc_message, signature)

    signature = RSA_decrypt(deque(enc_message), deque(d_a), deque(n_a))
    return (enc_message, signature)

def alice(n_a, n_b, e_b, d_a, msg_fmt, message_no):
    return sign_message(n_a, n_b, e_b, d_a, msg_fmt, message_no)

def fake_alice(n_e, n_b, e_b, d_e, msg_fmt, message_no):
    return sign_message(n_e, n_b, e_b, d_e, msg_fmt, message_no)

def bob(cryptogram, n_a, e_a, n_b, d_b):
    """
     Receives the cryptogram and verifies if the authenticity of the signature

    Word-RAM complexities: consider n_a, e_a, cryptogram.0, cryptogram.1 the effective numbers (deque digits joined)
    - Time: O(logmax(e_a, d_b) * (logmax(cryptogram.1, e_a, d_b, cryptogram.0) ^ (log2(3)) + logmax(cryptogram.1, cryptogram.0, n_b, n_a) ^ 2) + logmax(cryptogram.0, cryptogram.1))
    - Space: O(logmax(cryptogram.0, cryptogram.1))
    Real-RAM complexities: consider n_a, e_a, cryptogram.0, cryptogram.1 the effective numbers (deque digits joined)
    - Time: O(logmax(e_a, cryptogram.0, d_b, cryptogram.1))
    - Space: O(logmax(cryptogram.0, cryptogram.1))

    :param cryptogram: (Ceb(M), Da(Ceb(M))) or (Ceb(M), Ceb(Da(M)))
    :param n_a: Description
    :param e_a: Description
    """
    if n_a > n_b:
        enc_message = RSA_encrypt(''.join(map(str, cryptogram[1])), deque(e_a), deque(n_a))
        message1 = ''.join(map(str, cryptogram[0]))
        message2 = ''.join(map(str, enc_message))
        return message1 == message2

    message1 = RSA_decrypt(cryptogram[0], deque(d_b), deque(n_b))
    message2 = RSA_decrypt(cryptogram[1], deque(d_b), deque(n_b))
    message2 = RSA_encrypt(message2, deque(e_a), deque(n_a))
    return message1 == message2

def digital_signature_init(afile1, afile2, bfile1, bfile2, efile1, efile2):
    print("DIGITAL SIGNATURE ALGORITHM:")

    print("For simplification, the signature will be done on the whole message")
    print("This process is not seen in practice where cryptograms are (cb(m), sign(hash(m)))")
    print("Public and secret information for visualizing purposes:")
    # Alice
    n_a, e_a, d_a = RSA_crypto_system(False, "", afile1, afile2)
    # Bob
    n_b, e_b, d_b = RSA_crypto_system(False, "", bfile1, bfile2)
    # Eve
    n_e, e_e, d_e = RSA_crypto_system(False, "", efile1, efile2)
    print("Alice RSA cryptosystem: " + "\nn_a = " + ''.join(map(str, n_a)) + "\ne_a = " + ''.join(map(str, e_a)) + "\nd_a = " + ''.join(map(str, d_a)))
    print("Bob RSA cryptosystem: " + "\nn_b = " + ''.join(map(str, n_b)) + "\ne_b = " + ''.join(map(str, e_b)) + "\nd_b = " + ''.join(map(str, d_b)))
    print("Eve RSA cryptosystem: " + "\nn_e = " + ''.join(map(str, n_e)) + "\ne_e = " + ''.join(map(str, e_e)) + "\nd_e = " + ''.join(map(str, d_e)))

    message = input("Plaintext message that Alice will send to Bob: ")
    message_no = str(convert_plaintext_to_number(message))
    msg_fmt = deque()
    for cm in message_no:
        msg_fmt.append(int(cm))

    print("Alice sends the cryptogram to Bob:")
    alice_cryptogram = alice(n_a, n_b, e_b, d_a, msg_fmt, message_no)
    if bob(alice_cryptogram, n_a, e_a, n_b, d_b):
        print("Bob detects that Alice's cryptogram (" + ''.join(map(str, alice_cryptogram[0])) + ", " + ''.join(map(str, alice_cryptogram[1])) + ") is from ALICE!")
    else:
        print("Bob detects that Alice's cryptogram (" + ''.join(map(str, alice_cryptogram[0])) + ", " + ''.join(map(str, alice_cryptogram[1])) + ") is from EVE!")

    print("Eve sends the cryptogram to Bob:")
    fake_alice_cryptogram = fake_alice(n_e, n_b, e_b, d_e, msg_fmt, message_no)
    if bob(fake_alice_cryptogram, n_a, e_a, n_b, d_b):
        print("Bob detects that Eve's cryptogram (" + ''.join(map(str, fake_alice_cryptogram[0])) + ", " + ''.join(map(str, fake_alice_cryptogram[1])) + ") is from ALICE!")
    else:
        print("Bob detects that Eve's cryptogram (" + ''.join(map(str, fake_alice_cryptogram[0])) + ", " + ''.join(map(str, fake_alice_cryptogram[1])) + ") is from EVE!")

digital_signature_init("ds_rsa_p1_prime", "ds_rsa_q1_prime", "ds_rsa_p2_prime", "ds_rsa_q2_prime", "ds_rsa_p3_prime", "ds_rsa_q3_prime")
# digital_signature_init("ds_rsa_p1_prime", "ds_rsa_q1_prime", "ds_rsa_p3_prime", "ds_rsa_q3_prime", "ds_rsa_p2_prime", "ds_rsa_q2_prime")
# digital_signature_init("ds_rsa_p2_prime", "ds_rsa_q2_prime", "ds_rsa_p1_prime", "ds_rsa_q1_prime", "ds_rsa_p3_prime", "ds_rsa_q3_prime")
# digital_signature_init("ds_rsa_p2_prime", "ds_rsa_q2_prime", "ds_rsa_p3_prime", "ds_rsa_q3_prime", "ds_rsa_p1_prime", "ds_rsa_q1_prime")
# digital_signature_init("ds_rsa_p3_prime", "ds_rsa_q3_prime", "ds_rsa_p1_prime", "ds_rsa_q1_prime", "ds_rsa_p2_prime", "ds_rsa_q2_prime")
# digital_signature_init("ds_rsa_p3_prime", "ds_rsa_q3_prime", "ds_rsa_p2_prime", "ds_rsa_q2_prime", "ds_rsa_p1_prime", "ds_rsa_q1_prime")