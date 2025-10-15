from bitstring import BitArray

KEY = 107
REGISTER_LENGTH = 4
TAP_BIT_POSITIONS = [0, 3]
TICKS = 15

# Allows the stream to 'grow' as long as you like
def int_to_bitstring(my_int):
    my_bits = bin(my_int)[2:]
    return my_bits

class LFSR:
    def __init__(self, key: int, key_length: int, tap_bit_positions: list):
        # Validation
        if not isinstance(key, int):
            raise TypeError("Key must be an integer")
        if not isinstance(key_length, int):
            raise TypeError("Key length must be an integer")
        if (not isinstance(tap_bit_positions, list) or
                not all(isinstance(items, int) for items in tap_bit_positions)):
            raise TypeError("tap_bit_positions must be a list of integers")
        if len(tap_bit_positions) < 2:
            raise ValueError("You must provide at least two tap bit positions")

        self.state = key
        self.key_length = key_length
        self.tap_bit_positions = tap_bit_positions
        self.stream = 0
        self.cycles = 0

    # Preserves the length of the original bitstring, so the key can display properly
    def int_to_bitstring_preserve_length(self, my_int):
        # Convert the integer to a BitArray
        my_bits = BitArray(uint=my_int, length=self.key_length)
        # Return the BitArray as a binary string
        return my_bits.bin

    def bitstring_to_int(self, my_bits):
        # Convert the binary string into a BitArray
        my_bits = BitArray(bin=my_bits, length=self.key_length)
        # Return the BitArray as a two's complement unsigned integer
        return my_bits.uint

    def read_stream_bit(self):
        # Bitwise AND to ignore everything except the first bit
        return self.state & 1

    # Creates a 'mask' (the 1) and shifts it to the position specified so the bit can be read using bitwise AND
    def read_tap_bit(self, bit_position):
        bit_pos = (1 << bit_position)
        output = self.state & bit_pos
        if output == 0:
            return 0
        else:
            return 1

    # Apparently the stream bit doesn't have to form part of the feedback bit calculation
    def calculate_feedback_bit(self):
        # ^ (XOR)
        fb_bit = 0
        for pos in self.tap_bit_positions:
            tp_bit = self.read_tap_bit(pos)
            fb_bit ^= tp_bit
        return fb_bit

    # Shifts the whole register right once so the stream bit drops off the end
    def shift_register(self):
        self.state >>= 1

    def insert_feedback_bit(self, fb_bit):
        fb_bit_pos = fb_bit << (self.key_length - 1) # -1 to account for positions starting a zero
        self.state |= fb_bit_pos

    # Shifts the stream left and uses bitwise OR to append the new stream bit
    def append_to_stream(self, st_bit):
        self.stream <<= 1
        self.stream |= st_bit

    # Single pass of the LFSR algorithm, outputting to the terminal
    def clock_verbose(self):
        state_bin_str = self.int_to_bitstring_preserve_length(self.state)
        print(f"Binary representation of the key register: {state_bin_str}")
        stream_bit = self.read_stream_bit()
        print(f"Stream bit: {stream_bit}")
        feedback_bit = self.calculate_feedback_bit()
        print(f"Feedback bit: {feedback_bit}")
        self.shift_register()
        shifted_state_bin_str = self.int_to_bitstring_preserve_length(self.state)
        print(f"Binary representation of the shifted key register: {shifted_state_bin_str}")
        self.insert_feedback_bit(feedback_bit)
        updated_reg_bin_str = self.int_to_bitstring_preserve_length(self.state)
        print(f"Binary representation of the updated key register: {updated_reg_bin_str}")
        self.append_to_stream(stream_bit)
        stream_bin_str = int_to_bitstring(self.stream)
        print(f"Binary representation of the updated stream: {stream_bin_str}")
        if self.state == KEY:
            self.cycles += 1
            print("CYCLE DETECTED!")
        print("------------------------------------------------------------")
        return self.state, self.stream, self.cycles

    # Single pass of the LFSR algorithm, only returning the next stream bit
    def clock(self):
        stream_bit = self.read_stream_bit()
        feedback_bit = self.calculate_feedback_bit()
        self.shift_register()
        self.insert_feedback_bit(feedback_bit)
        return stream_bit


if __name__ == '__main__':
    lfsr = LFSR(KEY, REGISTER_LENGTH, TAP_BIT_POSITIONS)
    for i in range(TICKS):
        print(f"Pass number {i + 1}")
        key_reg, stream, cycles = lfsr.clock_verbose()
    print(f"Cycles: {lfsr.cycles}")
