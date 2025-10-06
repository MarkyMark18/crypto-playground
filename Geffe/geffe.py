from Geffe import lfsr

KEYS = [3, 7, 10]
KEY_LENGTHS = [4, 4, 4]
TAPS = [[0, 2], [0, 3], [0, 1]]
LOOPS = 15

class GeffeGenerator:

    def __init__(self, keys: list[int], key_lengths: list[int], taps: list[list[int]]):

        # Validation
        if not isinstance(keys, list) or not all(isinstance(items, int) for items in keys):
            raise TypeError("keys must be a list of ints")
        if not isinstance(key_lengths, list) or not all(isinstance(items, int) for items in key_lengths):
            raise TypeError("key_lengths must be a list of ints")
        if (not isinstance(taps, list) or
                not all(isinstance(sublist, list) and
                        all(isinstance(item, int) for item in sublist) for sublist in taps)):
            raise TypeError("taps must be a list of lists of ints")

        self.keys = keys
        self.key_lengths = key_lengths
        self.taps = taps
        self.stream = 0
        self.lfsr_multi = lfsr.LFSR(self.keys[0], self.key_lengths[0], self.taps[0])
        self.lfsr_1 = lfsr.LFSR(self.keys[1], self.key_lengths[1], self.taps[1])
        self.lfsr_2 = lfsr.LFSR(self.keys[2], self.key_lengths[2], self.taps[2])

    def append_to_stream(self, st_bit):
        self.stream <<= 1
        self.stream |= st_bit

    def clock(self):
        stream_bit_multi = self.lfsr_multi.clock()
        stream_bit_1 = self.lfsr_1.clock()
        stream_bit_2 = self.lfsr_2.clock()
        if stream_bit_multi == 0:
            print("Outputting from LFSR1")
            self.append_to_stream(stream_bit_1)
            return stream_bit_1
        else:
            print("Outputting from LFSR2")
            self.append_to_stream(stream_bit_2)
            return stream_bit_2

if __name__ == "__main__":
    geffe = GeffeGenerator(KEYS, KEY_LENGTHS, TAPS)
    for i in range(LOOPS):
        stream_bit = geffe.clock()
        print(f"Latest stream bit: {stream_bit}")
        print(f"The current stream is: {bin(geffe.stream)[2:]}")
        print("------------------------------------------------")