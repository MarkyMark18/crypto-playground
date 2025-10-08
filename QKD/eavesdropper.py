import random

class Eavesdropper:
    def __init__(self):
        self.measured_photons = []

    def measure_photons(self, recd_photons):
        for i in range(len(recd_photons)):
            basis_int = random.randint(0, 1)
            basis = '+' if basis_int == 1 else 'x'
            if basis == recd_photons[i][1]:
                self.measured_photons.append(recd_photons[i])
            else:
                random_bit = random.randint(0, 1)
                self.measured_photons.append((random_bit, basis))

    def retransmit_photons(self):
        return self.measured_photons

if __name__ == '__main__':
    pass