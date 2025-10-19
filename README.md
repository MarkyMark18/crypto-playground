# Crypto Playground

Python implementations of cryptographic algorithms from my 'Cybersecurity in Action' and 'Introduction to Cryptography' modules at university.

**DISCLAIMER:** This repository is for educational purposes only. The code is not intended for production use and has not been vetted for security vulnerabilites.

---

## Features

Currently implemented:
*  Linear Feedback Shift Register (LFSR)
*  Geffe Generator
*  Divide and Conquer attack on a Geffe Generator
*  Quantum Key Distribution (QKD) Simulation

---

## How to Run

There are two ways to run the simulations:

1) Each algorithm is in its own module. To run the Geffe Generator, for example, you would enter:

```sh
python geffe.py
```

2) You can run the main interface which will allow you to run multiple demonstrations in a single 'session':

```sh
python main.py
```

## Editing Configurations

To configure the setup of the Geffe Generator/Divide and Conquer attack, you can edit geffeconfig.json, an example is shown below:

Note: For the divide and conquer attack to be successful, the configuration of the register lengths and taps must match the ones used to create the stream file

```sh
{
  "KEYS": [88, 201, 7821],
  "REGISTER_LENGTHS": [7, 11, 13],
  "TAPS": [
    [0, 6],
    [0, 9],
    [0, 9, 10, 12]
  ],
  "BITS_TO_GENERATE": 2000,
  "FILENAME": "StreamFile.txt"
}
```

To configure the QKD simulation, you can edit qkdconfig.json, an example is shown below:

```sh
{
  "NO_OF_PHOTONS": 10000,
  "IS_EAVESDROPPED": true
}
```
