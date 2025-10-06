import random

class Sender:
    def __init__(self, num_photons):

        self.num_photons = num_photons
        self.photons = []

    def generate_photons(self):
        for i in range(self.num_photons):
            bit = random.randint(0, 1)
            basis_int = random.randint(0, 1)
            basis = '+' if basis_int == 1 else 'x'
            random_photon = (bit, basis)
            self.photons.append(random_photon)

    def send_photons(self):
        return self.photons


if __name__ == '__main__':
    alice = Sender(10)
    alice.generate_photons()
    print(alice.photons)