import random

class Sender:
    def __init__(self):

        self.photons = []
        self.kept_photons = []
        self.random_bit_indexes = []
        self.own_random_bits = []

    def generate_photons(self, num_photons):
        for i in range(num_photons):
            bit = random.randint(0, 1)
            basis_int = random.randint(0, 1)
            basis = '+' if basis_int == 1 else 'x'
            random_photon = (bit, basis)
            self.photons.append(random_photon)

    def send_photons(self):
        return self.photons

    def check_bases(self, recd_bases):
        for i in range(len(self.photons)):
            if self.photons[i][1] == recd_bases[i]:
                self.kept_photons.append(True)
            else:
                self.kept_photons.append(False)

    def announce_kept_photons(self):
        self.discard_photons()
        return self.kept_photons

    def discard_photons(self):
        discarded_no = 0
        for i in range(len(self.photons)):
            if not self.kept_photons[i]:
                self.photons.pop(i - discarded_no)
                discarded_no += 1

    def announce_random_bit_indexes(self):
        self.random_bit_indexes = random.sample(range(len(self.photons)), len(self.photons) // 2)
        for i in self.random_bit_indexes:
            self.own_random_bits.append(self.photons[i][0])
        return self.random_bit_indexes

    def is_there_eavesdropper(self, recd_random_bits):
        matching_bits = 0
        for i in range(len(self.own_random_bits)):
            if self.own_random_bits[i] == recd_random_bits[i]:
                matching_bits += 1

        error_rate = 1 - (matching_bits / len(recd_random_bits))
        print(f'Error rate: {error_rate}')
        if error_rate > 0.2:
            return True
        return False


if __name__ == '__main__':
    pass