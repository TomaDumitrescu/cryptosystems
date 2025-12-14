# Copyright 2025 -Toma Dumitrescu
from helpers import *

# Non-authorized accesses can be prevented by simulating encapsulation

class ElGamalEntity():
    def __init__(self, p: deque, g: deque, name: str):
        self.p = p
        self.g = g
        self.el_gamal = None
        _, p_diff = big_substract(deque(p), False, deque([2]), False)
        self.private_no = random_less_than(p_diff)
        self.communication_dests = {}
        self.val = -1
        self.name = name

    def set_el_gamal(self, el_gamal: "ElGamal"):
        self.el_gamal = el_gamal

    def broadcast(self):
        """
        Sends the public g ^ private_no mod p to the el gamal system to send to each participant

        Word-RAM complexities: consider g, private_no, p, val the effective numbers (deque digits joined)
        - Time: O(log2(private_no) * (logmax(g, private_no) ^ (log2(3)) + logmax(g, p) ^ 2)) + O(el_gamal.broadcast)
        - Space: O(logmax(g, private_no))
        Real-RAM complexities: consider g, private_no, p, val the effective numbers (deque digits joined)
        - Time: O(log(private_no)) + O(el_gamal.broadcast)
        - Space: O(1)

        :param self: The instance of ElGamalEntity
        """
        self.val = pow_mod(deque(self.g), deque(self.private_no), deque(self.p))
        print(self.name + " broadcasts " + ''.join(map(str, self.val)))
        self.el_gamal.broadcast(self.val, self)

    def send(self, dest, message):
        """
        Encrypts the message with a random generated key and sends to the el gamal system to send it to the dest

        Word-RAM complexities: consider g, c,  (deque digits joined)
        - Time: O(log2(p) * (logmax(c, g, p) ^ (log2(3)) + logmax(g, p) ^ 2)) + O(el_gamal.encrypt_send)
        - Space: O(logmax(message, p))
        Real-RAM complexities: consider g, private_no, p, val the effective numbers (deque digits joined)
        - Time: O(log(message)) + O(log(p)) + O(el_gamal.encrypt_send())
        - Space: O(log(message))

        :param self: the instance of ElGamalEntity
        :param dest: the destination as ElGamalEntity
        :param message: the message as string
        """
        if self.val == 0 or (not dest in self.communication_dests):
            return
        c = self.communication_dests[dest]
        print(self.name + " sent " + message + " to " + dest.name)
        message = str(convert_plaintext_to_number(message))
        msg_fmt = deque()
        for cm in message:
            msg_fmt.append(int(cm))

        rand_b = random_less_than(self.p)
        y1 = pow_mod(deque(self.g), deque(rand_b), deque(self.p))
        y2 = pow_mod(deque(c), rand_b, deque(self.p))
        _, y2 = big_multiply_dec(deque(y2), False, deque(msg_fmt), False)
        y2 = mod_big(y2, deque(self.p))
        self.el_gamal.encrypt_send(self, (y1, y2), dest)

    def receive(self, src, val):
        """
        Receives the public key and stores it by mapping to its origin

        Word-RAM complexities:
        - Time: O(1)
        - Space: O(1)
        Real-RAM complexities:
        - Time: O(1)
        - Space: O(1)

        :param self: the ElGamal entity
        :param src: the source
        :param val: the receive public key
        """
        print(self.name + " receives from " + src.name + " " + ''.join(map(str, val)))
        self.communication_dests[src] = val

    def receive_message(self, src, cryptogram):
        """
        Receives the message from src as number and converts it to text

        Word-RAM complexities: consider y1, y2, private_no the effective numbers (deque digits joined)
        - Time: O(log2(private_no) * (logmax(y1, y2, private_no, p) ^ (log2(3)) + logmax(y1, y2, private_no, p) ^ 2)) + O(el_gamal.encrypt_send)
        - Space: O(logmax(message, p))
        Real-RAM complexities: consider y1, y2, private_no the effective numbers (deque digits joined)
        - Time: O(log(private_no))
        - Space: O(log(message))

        :param self: the ElGamal Entity
        :param src: the source id
        :param cryptogram: the cryptogram as a tuple of two deques
        """
        y1, y2 = cryptogram[0], cryptogram[1]
        # If correct destination, then message should be clear
        z = pow_mod(deque(y1), deque(self.private_no), deque(self.p))
        # Fermat theorem
        _, p_diff2 = big_substract(deque(self.p), False, deque([2]), False)
        z_inv = pow_mod(z, p_diff2, self.p)
        # (a mod p) * (b mod p) mod p = (ab) mod p
        _, result = big_multiply_dec(y2, False, z_inv, False)
        result = mod_big(result, deque(self.p))
        message = int(''.join(map(str, result)))
        message_fmt = convert_number_to_plaintext(message)
        print(self.name + " received " + message_fmt + " from " + src.name)


class ElGamal():
    def __init__(self, p: deque, g: deque, participants: list):
        self.p = p
        self.g = g
        self.participants = participants
        for participant in participants:
            participant.set_el_gamal(self)

    def broadcast(self, val, src):
        """
        Docstring for broadcast

        Word-RAM complexities:
        - Time: O(len(participants))
        - Space: O(1)
        Real-RAM complexities:
        - Time: O(len(participants))
        - Space: O(1)

        :param self: Description
        :param val: Description
        :param src: Description
        """
        # participants can be filtered depending on src
        for p in self.participants:
            p.receive(src, val)

    def encrypt_send(self, src, cryptogram, dest):
        """
        Receives the encrypted message from the source and sends it to the dest

        Word-RAM complexities:
        - Time: O(maxlen(y1, y2)) + O(receive_message)
        - Space: O(maxlen(y1, y2))
        Real-RAM complexities:
        - Time: O(maxlen(y1, y2)) + O(receive_message)
        - Space: O(maxlen(y1, y2))

        :param self: the instance of ElGamal
        :param src: the source as ElGamalEntity
        :param cryptogram: tuple of twod eques
        :param dest: the dest as ElGamalEntity
        """
        y1, y2 = cryptogram[0], cryptogram[1]
        y1_str = ''.join(map(str, y1))
        y2_str = ''.join(map(str, y2))
        print("El Gamal encrypted the message from " + src.name + " to " + dest.name + " as (" + y1_str + ", " + y2_str + ")")
        dest.receive_message(src, cryptogram)

def el_gamal_presentation(filename):
    _, p = get_number(filename)
    g = deque(random.choices([2, 5]))

    print("Public information:")
    print("g =", ''.join(map(str, g)))
    print("Prime p was generated using openssl prime -generate -bits 512 -safe")
    print("For modern standards 2048 bits, there should be optimizations such as Chinese Reminder Theorem")
    print("p =", ''.join(map(str, p)))

    # Initializing participants
    alice = ElGamalEntity(p, g, "Alice")
    bob = ElGamalEntity(p, g, "Bob")
    david = ElGamalEntity(p, g, "David")
    sam = ElGamalEntity(p, g, "Sam")

    participants = [alice, bob, david, sam]

    # Initializing El Gamal channel
    ElGamal(p, g, participants)

    print("Secret information:")
    # Broadcast phase
    print("BROADCAST STEP")
    for participant in participants:
        participant.broadcast()

    print("EXCHANGE MESSAGES")
    alice.send(david, "Hello, David!")
    sam.send(alice, "Hello, Alice!")
    david.send(sam, "Hello, Sam!")

el_gamal_presentation("el_gamal_prime")
