# Copyright 2025 -Toma Dumitrescu
from helpers import *

class PrivateKeyCalculator:
    def calculate_personal_no(self, p: deque):
        """
        Calculates a random in (1, p) open interval

        Word-RAM complexities: consider p the effective number (deque digits joined)
        - Time: ~~~ log(p) * number_of-tries ~~~ O(log(p) * (99...9 with log(p) digits - log(p))
        - Space: O(log p)
        Real-RAM complexities: consider p the effective number (deque digits joined)
        - Time: O(1)
        - Space: O(1)

        :param self: PrivateKeyCalculator instance
        :param p: the DH public key prime p as a deque
        """
        return random_less_than(p)

    def calculate_private_key(self, val: deque, private_no: deque, p: deque):
        """
        Calculates the shared private key between the two entities for each entity, called from the entity

        Word-RAM complexities: consider val, p, private_no the effective numbers (deque digits joined)
        - Time: O(log2(private_no) * logmax(a, b) ^ (log2(3)))
        - Space: O(logmax(val, private_no))
        Real-RAM complexities: consider val, p, private_no the effective numbers (deque digits joined)
        - Time: O(log(private_no))
        - Space: O(1)

        :param self: PrivateCalculator instance
        :param val: public key from other entity g ^ entity_private_no mod p, but as a deque
        :param private_no: communication entity private number as deque
        :param p: the prime p as a deque
        """
        return pow_mod(val, private_no, deque(p))

class DiffieHellmanEntity():
    def __init__(self, p: deque, g: deque, name: str):
        self.name = name
        self.p = p
        self.g = g
        self.calculator = PrivateKeyCalculator()

        # private field
        self.__private_no = self.calculator.calculate_personal_no(p)
        self.__private_key = None

    def send(self, dh: "DiffieHellmanEntity"):
        dh.receive(pow_mod(self.g, self.__private_no, self.p))

    def receive(self, val):
        print(self.name + " received " + ''.join(map(str, val)))
        self.__private_key = self.calculator.calculate_private_key(val, self.__private_no, self.p)

    # Temporary method
    def debug_private_key(self):
        print(self.name + " random number: " + ''.join(map(str, self.__private_no)))
        print(self.name + " key: " + ''.join(map(str, self.__private_key)))


def diffie_hellman(filename: str):
    # initialization
    print("DIFFIE-HELLMAN PROTOCOL\n")
    g_no = random.choice([2, 5])
    g = deque([g_no])
    _, p = get_number(filename)

    print("Public information:")
    print("g =", ''.join(map(str, g)))
    print("Prime p was generated using openssl prime -generate -bits 512 -safe")
    print("For modern standards 2048 bits, there should be optimizations such as Chinese Reminder Theorem")
    print("p =", ''.join(map(str, p)))

    # calculating private numbers a and b
    alice = DiffieHellmanEntity(p, g, "Alice")
    bob = DiffieHellmanEntity(p, g, "Bob")

    # Sending encoded private numbers based on the NP-hard problem of factoring
    alice.send(bob)
    bob.send(alice)

    # Display secret values for debugging purposes
    print("Secret and public information:")
    alice.debug_private_key()
    bob.debug_private_key()


diffie_hellman("dh_p_prime")