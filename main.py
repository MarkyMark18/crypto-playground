import Geffe.geffe as g
import Geffe.divide_and_conquer as d
import QKD.qkd as q
import json

def load_geffe_config():
    # Load the configuration
    try:
        with open("Geffe/geffeconfig.json", "r") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        print("Error: geffeconfig.json not found")
        exit(1)
    except json.JSONDecodeError:
        print("Error: geffeconfig.json is not a valid JSON")
        exit(1)
    return cfg

def load_qkd_config():
    # Load the configuration
    try:
        with open("QKD/qkdconfig.json", "r") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        print("Error: qkdconfig.json not found")
        exit(1)
    except json.JSONDecodeError:
        print("Error: qkdconfig.json is not a valid JSON")
        exit(1)
    return cfg

# Runs a Geffe Generator
def run_geffe():
    # Load the configuration
    config = load_geffe_config()
    keys = config["KEYS"]
    register_lens = config["REGISTER_LENGTHS"]
    taps = config["TAPS"]
    bits_to_generate = config["BITS_TO_GENERATE"]
    output_file = config["FILENAME"]

    print("")
    print("A demonstration of a Geffe Generator")
    print("To change the configuration of the Geffe Generator, edit geffeconfig.json")
    print("")
    print("The Keys")
    print(f"LFSR1 (Multiplexer): {keys[0]}")
    print(f"LFSR2 (Output 1): {keys[1]}")
    print(f"LFSR3 (Output 2): {keys[2]}")
    print("")
    print("The Register Lengths")
    print(f"LFSR1 (Multiplexer): {register_lens[0]}")
    print(f"LFSR2 (Output 1): {register_lens[1]}")
    print(f"LFSR3 (Output 2): {register_lens[2]}")
    print("")
    print("The Taps")
    print(f"LFSR1 (Multiplexer): {taps[0]}")
    print(f"LFSR2 (Output 1): {taps[1]}")
    print(f"LFSR3 (Output 2): {taps[2]}")
    print("")

    # Create the Geffe Generator
    geffe = g.GeffeGenerator(
        keys=keys,
        register_lengths=register_lens,
        taps=taps
    )

    # Generate the stream
    for i in range(bits_to_generate):
        geffe.clock()

    # Output the results
    print("Generating stream...")
    geffe.output_stream_file(output_file)

# Runs the Divide and Conquer attack on the Geffe Generator
def run_divide_and_conquer():
    # Load the configuration
    config = load_geffe_config()
    register_lens = config["REGISTER_LENGTHS"]
    taps = config["TAPS"]
    input_file = config["FILENAME"]

    # Create the divide and conquer setup
    div = d.DivAndConqLfsr(
        l1_reg_len=register_lens[0],
        l1_taps=taps[0],
        l2_reg_len=register_lens[1],
        l2_taps=taps[1],
        l3_reg_len=register_lens[2],
        l3_taps=taps[2]
    )

    # Open the stream file and carry out the attack
    print("")
    print("A demonstration of a divide and conquer attack on a Geffe Generator")
    print("To change the configuration of the Geffe Generator, edit geffeconfig.json")
    print("NOTE: In order for attack to be successful, the configuration of the register lengths and taps must match")
    print("      the ones used to generate the bit stream")
    print("")
    print("The Register Lengths")
    print(f"LFSR1 (Multiplexer): {register_lens[0]}")
    print(f"LFSR2 (Output 1): {register_lens[1]}")
    print(f"LFSR3 (Output 2): {register_lens[2]}")
    print("")
    print("The Taps")
    print(f"LFSR1 (Multiplexer): {taps[0]}")
    print(f"LFSR2 (Output 1): {taps[1]}")
    print(f"LFSR3 (Output 2): {taps[2]}")
    print("")

    div.load_stream_file(input_file)
    l1_key, l2_key, l3_key = div.get_multiplexer_lfsr_key()
    print("\n-------- RESULTS --------")
    print(f"LFSR1 Key: {l1_key}")
    print(f"LFSR2 Key: {l2_key}")
    print(f"LFSR3 Key: {l3_key}")

def run_qkd():
    # Load the configuration
    config = load_qkd_config()
    no_of_photons = config["NO_OF_PHOTONS"]
    is_eavesdropped = config["IS_EAVESDROPPED"]

    print("")
    print("A simulation of Quantum Key Distribution")
    print("To change the configuration of the QKD simulation, edit qkdconfig.json")
    print("")

    qkd = q.Qkd()
    qkd.simulate_qkd(no_of_photons, is_eavesdropped)

if __name__ == '__main__':
    while True:
        print("")
        print("|-------------------------------------|")
        print("|          CRYPTO PLAYGROUND          |")
        print("|-------------------------------------|")
        print("")
        print("Please select from the following options:")
        print("1) Create and run a Geffe Generator, outputting the stream to a file")
        print(
            "2) Run a divide and conquer attack on a stream file, to find the keys to the LFSRs that make up the Geffe Generator")
        print("3) Run a Quantum Key Distribution simulation")
        print("4) Quit the program")
        selection = int(input("> "))
        match selection:
            case 1:
                run_geffe()
            case 2:
                run_divide_and_conquer()
            case 3:
                run_qkd()
            case 4:
                exit()
            case _:
                print("Invalid selection")
