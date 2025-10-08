import random

class Receiver:
    def __init__(self):

        self.measured_photons = []
        self.random_bit_indexes = []

    def measure_photons(self, recd_photons):
        for i in range(len(recd_photons)):
            basis_int = random.randint(0,1)
            basis = '+' if basis_int == 1 else 'x'
            if basis == recd_photons[i][1]:
                self.measured_photons.append(recd_photons[i])
            else:
                random_bit = random.randint(0, 1)
                self.measured_photons.append((random_bit, basis))

    def announce_bases(self):
        bases = []
        for photon in self.measured_photons:
            bases.append(photon[1])
        return bases

    def discard_photons(self, kept_photons):
        discarded_no = 0
        for i in range(len(self.measured_photons)):
            if not kept_photons[i]:
                self.measured_photons.pop(i - discarded_no)
                discarded_no += 1

    def receive_random_bit_indexes(self, random_bit_indexes):
        self.random_bit_indexes = random_bit_indexes

    def announce_random_bits(self):
        random_bits = []
        for i in self.random_bit_indexes:
            random_bits.append(self.measured_photons[i][0])
        return random_bits


if __name__ == '__main__':
    pass