# Crypto Playground

Python implementations of cryptographic algorithms from my 'Cybersecurity in Action' and 'Introduction to Cryptography' modules at university.

**DISCLAIMER:** This repository is for educational purposes only. The code is not intended for production use and has not been vetted for security vulnerabilites.

---

## Features

Currently implemented:
* Linear Feedback Shift Register (LFSR)
*  Geffe Generator

---

## How to Run

Each algorithm is in its own module. To run the Geffe Generator, for example, you would enter:

```sh
python geffe.py
```

They currently have hardcoded parameters such as initial keys, taps and register lengths at the top of the .py files, however in the future I plan to make a script that will allow you to change these without editing the file.

**Example Output (geffe.py):**

```
Outputting from LFSR2
Latest stream bit: 0
The current stream is: 0
------------------------------------------------
Outputting from LFSR2
Latest stream bit: 1
The current stream is: 1
------------------------------------------------
Outputting from LFSR1
Latest stream bit: 1
The current stream is: 11
------------------------------------------------
Outputting from LFSR1
Latest stream bit: 0
The current stream is: 110
------------------------------------------------
...
```
