from LinearCryptanalysis import LATGenerator


class LinearCryptanalysis:
    def __init__(self):
        self._lat_gen = LATGenerator.LATGenerator()
        self._lat = self._lat_gen.calculate_lat()
        self._threshold = 2
        self._linear_approximations = []

    def print_lat(self):
        self._lat_gen.print_lat()

    def linear_approximation_search(self, threshold=2):
        self._threshold = threshold
        self._round_1()

        if len(self._linear_approximations) == 0:
            print("There are no valid linear approximations using the provided threshold")

        for i, approx in enumerate(self._linear_approximations):
            print(f"Linear Approximation: {i}")
            print(f"    X_1 Mask: {approx['x_1_mask']}")
            print(f"    Y_1 Mask: {approx['y_1_mask']}")
            print(f"    Y_2 Mask: {approx['y_2_mask']}")
            print(f"    Round 1 Bias: {approx['round_1_bias']}")
            print(f"    Round 2 Bias: {approx['round_2_bias']}")
            print(f"    Combined Probability: {approx['combined_probability']}")

    def _round_1(self):
        for x_mask in range(16):
            for y_mask in range(16):
                # Ignore the top left entry in the table as (0,0) is always +8 bias
                if x_mask == 0 and y_mask == 0:
                    continue

                # Grab the bias from the LAT
                bias = self._lat[x_mask][y_mask]
                if abs(bias) > self._threshold:
                    # Move to the next round of the cipher
                    self._round_2(x_mask, y_mask, bias)

    def _round_2(self, x_1_mask, y_1_mask, bias_1):
        # Start search from the row in the LAT associated with the output of the first round
        for y_2_mask in range(16):
            # Grab the bias from the LAT
            bias_2 = self._lat[y_1_mask][y_2_mask]
            if abs(bias_2) > self._threshold:
                # Calculate the combined probability using Matsui's Piling Up Lemma
                combined_probability = 0.5 + 2 * (bias_1 / 16) * (bias_2 / 16)
                # Save the details as a viable linear approximation for later use
                self._linear_approximations.append({
                    "x_1_mask": x_1_mask,
                    "y_1_mask": y_1_mask,
                    "y_2_mask": y_2_mask,
                    "round_1_bias": bias_1,
                    "round_2_bias": bias_2,
                    "combined_probability": combined_probability
                })


if __name__ == "__main__":
    linear_crypt = LinearCryptanalysis()
    linear_crypt.print_lat()
    linear_crypt.linear_approximation_search(2)