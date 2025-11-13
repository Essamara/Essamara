# Quantum SWAP Gate (`workingswap.py`)

This script demonstrates the implementation of the quantum SWAP gate using a sequence of three CNOT (Controlled-NOT) gates.

## Description

The SWAP gate is a fundamental two-qubit quantum operation that, as its name suggests, swaps the quantum states of two qubits. If two qubits are in the states `|ψ⟩` and `|φ⟩`, the SWAP gate transforms them to `|φ⟩` and `|ψ⟩`.

This script shows a common and efficient way to construct a SWAP gate using only CNOT gates, which are often more readily available on quantum hardware. The specific decomposition used is:
`SWAP(A, B) = CNOT(A, B) * CNOT(B, A) * CNOT(A, B)`

The script tests this implementation for three different initial states—`|10⟩`, `|01⟩`, and `|11⟩`—to verify that it correctly swaps the qubit states in all cases.

## How It Works

The `swap_kernel` function defines the quantum circuit:
1.  **Qubit Allocation and Initialization**: Two qubits, `a_qubit` and `b_qubit`, are allocated and initialized to the classical input values (`0` or `1`).
2.  **SWAP Gate Decomposition**: Three consecutive CNOT gates are applied to the two qubits in the specific sequence required to perform the swap.
3.  **Measurement**: Both qubits are measured to determine their final states after the swap operation.

The `run_swap_test` function then drives the execution for a given pair of input values, compares the measured result to the expected swapped result, and prints a clear "SUCCESS" or "FAILURE" message.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python workingswap.py
```
The script will automatically run the three predefined test cases:
- Swapping `|10⟩` to `|01⟩`
- Swapping `|01⟩` to `|10⟩`
- Swapping `|11⟩` to `|11⟩` (which remains unchanged)

For each test, it will print the initial state, the final measured state, and whether the swap operation was successful, providing a clear verification of the SWAP gate's functionality.
