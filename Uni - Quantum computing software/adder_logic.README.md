# 8-Bit Quantum Stream (`adder_logic.py`)

This script demonstrates how to generate an 8-bit random binary number using an 8-qubit quantum circuit.

## Description

This script leverages the principle of superposition to create a simple but effective quantum random number generator. It initializes an 8-qubit register and applies a Hadamard gate to each qubit, putting them all into a superposition of |0> and |1>. When measured, each qubit collapses to a definite state, resulting in a random 8-bit binary string.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How It Works

The `eight_bit_stream` kernel performs the following steps:
1.  **Allocation**: Allocates an 8-qubit register.
2.  **Superposition**: Applies a Hadamard gate to each of the 8 qubits in parallel.
3.  **Measurement**: Measures the entire 8-qubit register.

The script then executes this kernel 1000 times (the default number of shots) and prints the top 5 most frequent results, along with the single most probable outcome.

## How to Run
```bash
python adder_logic.py
```
The script will display the probability distribution of the measurement results and the most likely 8-bit random number.
