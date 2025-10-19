import json
from Geffe import lfsr

class GeffeGenerator:

    def __init__(self, keys: list[int], register_lengths: list[int], taps: list[list[int]]):

        # Validation
        if not isinstance(keys, list) or not all(isinstance(items, int) for items in keys):
            raise TypeError("keys must be a list of ints")
        if not isinstance(register_lengths, list) or not all(isinstance(items, int) for items in register_lengths):
            raise TypeError("key_lengths must be a list of ints")
        if (not isinstance(taps, list) or
                not all(isinstance(sublist, list) and
                        all(isinstance(item, int) for item in sublist) for sublist in taps)):
            raise TypeError("taps must be a list of lists of ints")

        self.keys = keys
        self.register_lengths = register_lengths
        self.taps = taps
        self.stream = 0
        self.lfsr_multi = lfsr.LFSR(self.keys[0], self.register_lengths[0], self.taps[0])
        self.lfsr_1 = lfsr.LFSR(self.keys[1], self.register_lengths[1], self.taps[1])
        self.lfsr_2 = lfsr.LFSR(self.keys[2], self.register_lengths[2], self.taps[2])

    def append_to_stream(self, st_bit):
        self.stream <<= 1
        self.stream |= st_bit

    def output_stream_file(self, filename):
        print(f"Outputting stream to file: {filename}")
        with open(filename, "w") as sf:
            for bit in bin(self.stream)[2:]:
                sf.write(str(bit) + " ")

    # Runs a single 'tick' of the Geffe Generator and outputs a stream bit
    def clock(self):
        stream_bit_multi = self.lfsr_multi.clock()
        stream_bit_1 = self.lfsr_1.clock()
        stream_bit_2 = self.lfsr_2.clock()
        if stream_bit_multi == 1:
            # print("Outputting from LFSR1")
            self.append_to_stream(stream_bit_1)
            return stream_bit_1
        else:
            # print("Outputting from LFSR2")
            self.append_to_stream(stream_bit_2)
            return stream_bit_2

if __name__ == "__main__":

    # Load the configuration
    try:
        with open("geffeconfig.json", "r") as jf:
            config = json.load(jf)
    except FileNotFoundError:
        print("Error: geffeconfig.json not found")
        exit(1)
    except json.JSONDecodeError:
        print("Error: geffeconfig.json is not a valid JSON")
        exit(1)

    bits_to_generate = config["BITS_TO_GENERATE"]
    output_file = config["FILENAME"]

    # Create the Geffe Generator
    geffe = GeffeGenerator(
        keys=config["KEYS"],
        register_lengths=config["REGISTER_LENGTHS"],
        taps=config["TAPS"]
    )

    # Generate the stream
    for i in range(bits_to_generate):
        stream_bit = geffe.clock()
        # print(f"Latest stream bit: {stream_bit}")
        # print(f"The current stream is: {bin(geffe.stream)[2:]}")
        # print("------------------------------------------------")

    # Output the results
    geffe.output_stream_file(output_file)