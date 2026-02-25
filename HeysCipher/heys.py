from HeysCipher import sbox, pbox

class HeysCipher:
    def __init__(self, rounds):
        self._rounds = rounds
        self._subkeys = []
        self._sbox = sbox.SBox()
        self._pbox = pbox.PBox()

    # Take in a master key, and split it into the subkeys used for each round
    def _generate_subkeys(self, master_key):
        self._check_master_key_length(master_key)
        subkeys = []
        mask = 0xFFFF
        for i in range(self._rounds + 1):
            subkeys.append(mask & master_key >> (16 * i))
        return subkeys

    # Validate that the master key is the correct length so there are no blank subkeys
    def _check_master_key_length(self, master_key):
        max_key_len = 16 * (self._rounds + 1)
        min_key_len = 16 * self._rounds
        key_len = master_key.bit_length()
        if key_len > max_key_len:
            raise ValueError(f"The master key is too long! Maximum key length is {max_key_len} bits for a {self._rounds} round cipher")
        elif key_len <= min_key_len:
            print("Warning... The Master Key is too short! Some Subkeys will be blank!")

    # Completes the subkey mixing step, where the input is XOR'd with the subkey
    def _subkey_mixing(self, inp, cipher_round):
        return inp ^ self._subkeys[cipher_round]

    # Encrypts a given plaintext using the supplied master key
    def encrypt(self, ptext, master_key):
        self._subkeys = self._generate_subkeys(master_key)
        round_result = [ptext]

        # Do Rounds 1 -> n - 1
        for round_index in range(self._rounds - 1):
            post_mix = self._subkey_mixing(round_result[-1], round_index)
            post_sbox = self._sbox.substitute(post_mix)
            post_perm = self._pbox.permutate(post_sbox)
            round_result.append(post_perm)

        # Do Round n
        last_round_mix = self._subkey_mixing(round_result[-1], self._rounds - 1)
        last_round_sbox = self._sbox.substitute(last_round_mix)
        round_result.append(last_round_sbox)

        # Do the final Subkey Mix
        final_mix = self._subkey_mixing(last_round_sbox, self._rounds)
        round_result.append(final_mix)

        return round_result[-1]

    # Decrypts a given ciphertext using the supplied master key
    def decrypt(self, ctext, master_key):
        self._subkeys = self._generate_subkeys(master_key)
        round_result = [ctext]

        # Reverse final Subkey Mix
        final_mix = self._subkey_mixing(round_result[-1], self._rounds)
        round_result.append(final_mix)

        # Reverse Round n
        last_round_sbox = self._sbox.inv_substitute(final_mix)
        last_round_mix = self._subkey_mixing(last_round_sbox, self._rounds - 1)
        round_result.append(last_round_mix)

        # Reverse Rounds n-1 -> 1
        for round_index in range(self._rounds - 2, -1, -1):
            post_perm = self._pbox.permutate(round_result[-1])
            post_sbox = self._sbox.inv_substitute(post_perm)
            post_mix = self._subkey_mixing(post_sbox, round_index)
            round_result.append(post_mix)

        return round_result[-1]


if __name__ == '__main__':
    heys = HeysCipher(4)

    initial_plaintext = 0xB49C
    key = 0xABCD01237654EF89A078

    print(f"Initial plaintext: {hex(initial_plaintext)}")

    ciphertext = heys.encrypt(initial_plaintext, key)

    print(f"Ciphertext: {hex(ciphertext)}")

    plaintext = heys.decrypt(ciphertext, key)

    print(f"Decrypted plaintext: {hex(plaintext)}")