# 8-Bit Quantum Superposition Test (`working8bit_superposition.py`)

This script demonstrates the principle of quantum superposition by performing an 8-bit XOR operation where one of the input bits exists in a superposition of both `0` and `1` simultaneously.

## Description

This script provides a clear and compelling example of one of the most fundamental and powerful concepts in quantum computing: superposition. It calculates the XOR sum of two 8-bit numbers, `A` and `B`, but with a quantum twist.

Before the XOR operation is performed, the least significant bit (LSB) of input `A` is placed into an equal superposition using a Hadamard gate. This means that for the duration of the computation, this bit is effectively both a `0` and a `1` at the same time.

As a result, the quantum computer calculates the XOR sum for both possibilities in parallel. When the output register is measured, it will collapse to one of the two possible classical outcomes with a roughly 50% probability for each.

## How It Works

1.  **State Preparation**: Two 8-qubit registers are initialized to the classical bit values of two input numbers, `A=4` and `B=5`.
2.  **Superposition**: A Hadamard gate is applied to the LSB of register A, putting it into a superposition. This effectively makes the value of A both 4 (`...0100`) and 5 (`...0101`) simultaneously.
3.  **Quantum XOR**: A series of CNOT gates are used to perform a bitwise XOR operation between the two registers, storing the result in the second register.
4.  **Measurement**: The output register (B) is measured.

Because the input `A` was in a superposition of 4 and 5, the measurement will yield one of two possible results:
-   `4 XOR 5 = 1`
-   `5 XOR 5 = 0`

The script runs the circuit multiple times (shots) and shows the statistical distribution of the outcomes, which should be very close to a 50/50 split between `0` and `1`.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working8bit_superposition.py
```
The script will execute the quantum circuit and print the expected outcomes. It will then display the actual measurement results from the simulation, showing the counts and probabilities for each outcome. A "SUCCESS" message is printed if both expected outcomes (`0` and `1`) are observed, confirming that the superposition was successfully created and utilized in the computation.
