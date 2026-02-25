

class SBox:
    def __init__(self):
        self._s_box = {
            0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
            0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
            0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
            0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7,
        }

        self._inv_s_box = {val: key for key, val in self._s_box.items()}

    # Splits the input into 4 nibbles
    @staticmethod
    def _split(full_inp):
        split_inp = []
        for i in range(4):
            mask = 0xF
            split_inp.append(mask & (full_inp >> i * 4))
        return split_inp

    # Reassembles the 4 nibbles back into a word
    @staticmethod
    def _reassemble(subs_inp):
        outp = 0
        for i in range(4):
            outp = outp | (subs_inp[i] << (i * 4))
        return outp

    # Completes a substitution step for a word (For encryption)
    def substitute(self, inp):
        inp_split = self._split(inp)
        outp_list = []
        for val in inp_split:
            outp_list.append(self._s_box[val])
        outp_int = self._reassemble(outp_list)
        return outp_int

    # Completes an inverse substitution step for a word (For Decryption/Linear Cryptanalysis)
    def inv_substitute(self, inp):
        inp_split = self._split(inp)
        outp_list = []
        for val in inp_split:
            outp_list.append(self._inv_s_box[val])
        outp_int = self._reassemble(outp_list)
        return outp_int

if __name__ == "__main__":
    s_box = SBox()
    inp_val = 0x5B0C
    print(hex(inp_val))
    outp_val = s_box.substitute(inp_val)
    print(hex(outp_val))
    rev_val = s_box.inv_substitute(outp_val)
    print(hex(rev_val))