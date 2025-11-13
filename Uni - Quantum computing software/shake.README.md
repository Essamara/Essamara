# Quantum-Seeded Hashing (`shake.py` and `cpushake.py`)

This directory contains two scripts that demonstrate how to generate a quantum-resistant hash using a seed produced by a quantum random number generator (QRNG).

## `shake.py`: Quantum-Resistant Hash Generation

This script generates a 256-bit quantum-resistant hash using the SHAKE256 algorithm, seeded with data from a simulated quantum circuit.

### Description

`shake.py` leverages the principles of quantum mechanics to produce a truly random seed for a cryptographic hash function. This is a key component in post-quantum cryptography (PQC), as it provides a source of entropy that is resistant to both classical and quantum attacks.

The process involves:
1.  **Quantum Random Number Generation**: A quantum circuit with Hadamard gates and a CNOT lattice is used to generate 8 bits of random data per run. This process is repeated 32 times to create a 256-bit seed.
2.  **Quantum-Resistant Hashing**: The 256-bit seed is fed into the SHAKE256 hash function, a member of the SHA-3 family, to produce a final 256-bit hash.

### Dependencies

- **Python 3.x**
- **Qiskit**: An open-source framework for quantum computing.

### How to Run
```bash
python shake.py
```
The script will print the generated quantum seed and the final quantum-resistant hash.

## `cpushake.py`: Quantum-Seeded Hashrate Tester

This script benchmarks the performance of the quantum-seeded hashing process by running it in an infinite loop and calculating the average hashrate.

### Description

`cpushake.py` uses the same quantum random number generation and hashing process as `shake.py`, but it is designed to measure how many quantum-resistant hashes can be generated per second. This is a useful metric for evaluating the practical performance of the QRNG-seeded hashing approach.

The script will continuously:
1.  Generate a 256-bit quantum random seed.
2.  Compute the SHAKE256 hash of the seed.
3.  Print the instantaneous hashrate.

When the script is stopped (with Ctrl+C), it will display the total number of hashes generated, the total time elapsed, and the average hashrate over the entire test.

### Dependencies

- **Python 3.x**
- **Qiskit**: An open-source framework for quantum computing.

### How to Run
```bash
python cpushake.py
```
The script will run indefinitely, printing the hashrate in real-time. Press `Ctrl+C` to terminate the script and view the final summary.
