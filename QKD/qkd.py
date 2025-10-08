from QKD import sender, receiver, eavesdropper

class QKD:
    def __init__(self):
        self.alice = sender.Sender()
        self.bob = receiver.Receiver()
        self.eve = eavesdropper.Eavesdropper()
        self.no_of_photons = 0
        self.matches = [0, 0, 0]
        self.is_eavesdropped = False
        self.eavesdropper_detected = False

    def simulate_qkd(self, no_of_photons, is_eavesdropped = False):
        # Set the number of photons and the presence of Eve
        self.no_of_photons = no_of_photons
        self.is_eavesdropped = is_eavesdropped

        # Alice generates a list of photons and their orientations
        self.alice.generate_photons(self.no_of_photons)

        # Alice sends the photons to Bob
        photons = self.alice.send_photons()

        # This is where Eve 'snoops' (If she's present)
        if self.is_eavesdropped:
            self.eve.measure_photons(photons)
            photons = self.eve.retransmit_photons()

        # Bob receives the photons and updates his list after measuring them
        self.bob.measure_photons(photons)

        # Bob sends his list of bases to Alice who checks them against her photons
        self.alice.check_bases(self.bob.announce_bases())

        # Alice announces her list of kept photons and both discard the others
        self.bob.discard_photons(self.alice.announce_kept_photons())

        # From the remaining photons, Alice sends the indexes of a random sample to Bob
        self.bob.receive_random_bit_indexes(self.alice.announce_random_bit_indexes())

        # Bob sends back the bits at the indexes on the list
        # Alice checks the bits against her own list, calculates the error rate and announces if there is an
        # eavesdropper!
        self.eavesdropper_detected = self.alice.is_there_eavesdropper(self.bob.announce_random_bits())
        print(f'Is there eavesdropper: {self.eavesdropper_detected}')


if __name__ == '__main__':
    qkd = QKD()
    qkd.simulate_qkd(100000, True)

