# 4-Bit Parallel CCNOT (`working16bit.py`)

This script demonstrates the parallel execution of four simultaneous CCNOT (Toffoli) gates using the CUDA-Q framework.

## Description

This script showcases a fundamental concept in quantum computation: the ability to perform parallel operations on multiple qubits. It implements a 4-bit parallel "AND" gate array, where four CCNOT gates are applied simultaneously.

The CCNOT gate, also known as the Toffoli gate, is a universal reversible logic gate, which means that any classical computation can be implemented using only CCNOT gates. It has two control qubits and one target qubit. The target qubit is flipped if and only if both control qubits are in the state |1>.

## How It Works

1.  **Qubit Allocation**: The script allocates a 16-qubit register, although only 12 are used for the 4-bit test (4 for control A, 4 for control B, and 4 for the target C).
2.  **State Preparation**: The eight control qubits (A and B) are all initialized to the |1> state. The four target qubits (C) are initialized to |0>.
3.  **Parallel CCNOT**: Four CCNOT gates are applied in parallel. The i-th CCNOT gate uses the i-th qubit from registers A and B as controls and the i-th qubit from register C as the target.
4.  **Measurement**: The four target qubits are measured.

Since all control qubits are set to |1>, the expected outcome is that all four target qubits will be flipped to |1>, resulting in the measurement of the state `1111`.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working16bit.py
```
The script will simulate the circuit and print the most probable measured state of the target qubits. It will then report whether the result matches the expected outcome (`1111`), confirming the successful parallel execution of the four CCNOT gates.
