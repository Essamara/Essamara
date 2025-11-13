# 4-Bit Grover's Search Oracle (`working4bitgrover.py`)

This script provides a detailed implementation of the oracle component for a 4-bit Grover's search algorithm, specifically targeting the state `|5>` (binary `0101`).

## Description

The oracle is the most critical part of Grover's algorithm. Its function is to "mark" the target state by applying a phase shift (multiplying it by -1), leaving all other states unchanged. This script demonstrates how to construct such an oracle for a 4-qubit system using the CUDA-Q framework.

A key challenge in building oracles for multi-qubit systems is the need for multi-controlled gates, which are not always natively supported by quantum hardware or simulators. This script addresses this by:

1.  **Decomposing the Toffoli (CCX) Gate**: It includes a `ccx_safe` kernel that breaks down the 3-qubit Toffoli gate into a sequence of more fundamental, universally supported gates (H, T, Tdg, CX).
2.  **Building a 4-Controlled NOT Gate**: Using the decomposed Toffoli gate as a building block, the main `grover_oracle_4bit_kernel` constructs a 4-controlled NOT gate with the help of ancilla qubits. This complex gate is what allows the oracle to selectively target a single state out of the 16 possible states in the 4-qubit system.
3.  **Uncomputation**: After the phase flip is applied, the script carefully reverses the operations on the ancilla qubits. This "uncomputation" is crucial to ensure that the ancilla qubits are returned to their initial state and do not interfere with the final measurement.

## How It Works

The script initializes the 4 data qubits into a uniform superposition of all 16 possible states. It then calls the oracle kernel, which performs the phase flip on the target state `|0101>`. Finally, it measures the data qubits.

**Note**: This script only implements the oracle, not the full Grover's search algorithm (which also requires a diffusion operator/amplification step). Therefore, running this script will **not** result in finding the target state with high probability. Instead, the measurement should yield a roughly uniform distribution of all 16 states. The purpose of this script is to verify that the complex oracle circuit can be successfully compiled and executed, which is a necessary first step before building the complete search algorithm.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working4bitgrover.py
```
The script will run the oracle on a superposition of all 4-qubit states and print the top 5 measurement results. You should see that the probabilities are all roughly equal, confirming that the oracle has run without collapsing the superposition to a single state.
