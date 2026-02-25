

class PBox:
    def __init__(self):
        # This is reversed to account for the Heys Cipher position numbering
        self._p_box = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]

    # Carries out a Permutation step for a word
    def permutate(self, inp):
        out = 0
        for bit_pos in range(16):
            bit_val = inp >> bit_pos & 1

            if bit_val == 1:
                out = out | 1 << self._p_box[bit_pos]
        return out


if __name__ == "__main__":
    p_box = PBox()
    inp_val = 0xAAAA
    out_val = p_box.permutate(inp_val)
    # Should be 0xF0F0
    print(hex(out_val))