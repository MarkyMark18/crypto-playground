from HeysCipher import sbox

class LATGenerator:
    def __init__(self):
        self._sbox = sbox.SBox()
        self._lat = [[0 for _ in range(16)] for _ in range(16)]

    def calculate_lat(self):
        # The "Input Sum" from Heys' paper
        for input_mask in range(16):
            # The "Output Sum" from Heys' paper
            for output_mask in range(16):
                matches = 0
                for sbox_input in range(16):
                    sbox_output = self._sbox.substitute(sbox_input)
                    input_parity = (sbox_input & input_mask).bit_count() % 2
                    output_parity = (sbox_output & output_mask).bit_count() % 2
                    matches += 1 if input_parity == output_parity else 0

                self._lat[input_mask][output_mask] = (matches - 8)

        return self._lat

    def print_lat(self):
        header = "   |"
        for i in range(16):
            header += f"{i:4X}"
        print(header)
        print("-" * 68)

        for row_index in range(16):
            row_str = f"{row_index:2X} |"
            for bias in self._lat[row_index]:
                if bias == 0:
                    row_str += "   0"
                elif bias > 0:
                    row_str += f"  +{bias}"
                else:
                    row_str += f"  {bias}"
            print(row_str)

        print()

if __name__ == "__main__":
    lat = LATGenerator()
    lat.calculate_lat()
    lat.print_lat()
