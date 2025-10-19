import json
from Geffe import lfsr


class DIV_AND_CONQ_LFSR:
    def __init__(self, l1_reg_len, l1_taps, l2_reg_len, l2_taps, l3_reg_len, l3_taps):
        # Params for LFSR1
        self.l1_key = 0
        self.l1_reg_len = l1_reg_len
        self.l1_taps = l1_taps
        # Params for LFSR2
        self.l2_key = 0
        self.l2_reg_len = l2_reg_len
        self.l2_taps = l2_taps
        # Params for LFSR3
        self.l3_key = 0
        self.l3_reg_len = l3_reg_len
        self.l3_taps = l3_taps

        self.check_bits = []

    def load_stream_file(self, stream_file):
        # Open the stream file and add the bits to a list
        print(f"Opening stream file: {stream_file}")
        with open(stream_file, "r") as f:
            stream_file = f.read().strip()
            self.check_bits = stream_file.split(" ")
            print(f"Stream contains {len(self.check_bits)} bits")
            for i in range(len(self.check_bits)):
                self.check_bits[i] = int(self.check_bits[i])

    # Get the key for a single output LFSR (LFSR 2/3)
    def get_output_lfsr_key(self, reg_len, taps):
        max_match = 0
        max_match_key = 0
        for key_attempt in range(2**reg_len):
            # Generate the stream
            l = lfsr.LFSR(key_attempt, reg_len, taps)
            stream = []
            for i in range(len(self.check_bits)):
                stream.append(l.clock())

            # Check the stream against the check bits (Should be ~75% match for correct key)
            stream_match = 0
            for i in range(len(self.check_bits)):
                if stream[i] == self.check_bits[i]:
                    stream_match += 1
            if stream_match > max_match:
                max_match = stream_match
                max_match_key = key_attempt
        print(f"The key is {max_match_key}")
        return max_match_key

    # Get the key for the multiplexer LFSR (LFSR1)
    def get_multiplexer_lfsr_key(self):
        # Get the keys for the two output LFSRs
        print("\nAttacking LFSR2")
        self.l2_key = self.get_output_lfsr_key(self.l2_reg_len, self.l2_taps)
        print("\nAttacking LFSR3")
        self.l3_key = self.get_output_lfsr_key(self.l3_reg_len, self.l3_taps)

        print("\nAttacking LFSR1")
        max_match = 0
        max_match_key = 0
        for key_attempt in range(2**self.l1_reg_len):
            # Generate the stream
            l1 = lfsr.LFSR(key_attempt, self.l1_reg_len, self.l1_taps)
            l2 = lfsr.LFSR(self.l2_key, self.l2_reg_len, self.l2_taps)
            l3 = lfsr.LFSR(self.l3_key, self.l3_reg_len, self.l3_taps)
            stream = []
            for i in range(len(self.check_bits)):
                sb1 = l1.clock()
                sb2 = l2.clock()
                sb3 = l3.clock()
                if sb1 == 0:
                    stream.append(sb3)
                else:
                    stream.append(sb2)

            # Check the stream against the check bits (Should be 100% match for correct key)
            stream_match = 0
            for i in range(len(self.check_bits)):
                if stream[i] == self.check_bits[i]:
                    stream_match += 1

            if stream_match > max_match:
                max_match = stream_match
                max_match_key = key_attempt

            self.l1_key = max_match_key

        print(f"The key is {max_match_key}")

        return self.l1_key, self.l2_key, self.l3_key


if __name__ == "__main__":

    # Load the configuration
    try:
        with open("geffeconfig.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: geffeconfig.json not found")
        exit(1)
    except json.JSONDecodeError:
        print("Error: geffeconfig.json is not a valid JSON")
        exit(1)

    register_lens = config["REGISTER_LENGTHS"]
    taps = config["TAPS"]
    input_file = config["FILENAME"]

    # Create the divide and conquer setup
    div = DIV_AND_CONQ_LFSR(
        l1_reg_len=register_lens[0],
        l1_taps=taps[0],
        l2_reg_len=register_lens[1],
        l2_taps=taps[1],
        l3_reg_len=register_lens[2],
        l3_taps=taps[2]
    )

    # Open the stream file and carry out the attack
    print("A demonstration of a divide and conquer attack on a Geffe Generator")
    div.load_stream_file(input_file)
    l1_key, l2_key, l3_key = div.get_multiplexer_lfsr_key()
    print("\n-------- RESULTS --------")
    print(f"LFSR1 Key: {l1_key}")
    print(f"LFSR2 Key: {l2_key}")
    print(f"LFSR3 Key: {l3_key}")