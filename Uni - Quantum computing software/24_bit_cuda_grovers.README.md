# 24-Qubit Grover's Search (`24_bit_cuda_grovers.py`)

This script implements a large-scale Grover's search algorithm for a 24-qubit system using the CUDA-Q framework.

## Description

This script demonstrates the power of quantum search on a significantly large search space of 2^24 (approximately 16.7 million) items. It is designed to find a single marked item, which in this implementation is the state where all qubits are |1> (`|11...1>`).

The script is composed of three main CUDA-Q kernels:
1.  **The Oracle (`grover_oracle`)**: This kernel marks the target state (`|11...1>`) by applying a multi-controlled Z gate.
2.  **The Diffuser (`grover_diffusion`)**: This kernel amplifies the probability of measuring the marked state.
3.  **The Main Search Circuit (`grover_search`)**: This kernel orchestrates the entire algorithm by initializing the qubits, applying the oracle and diffuser for the optimal number of iterations, and measuring the final state.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.
- **NumPy**: For numerical operations.

## How It Works

The script first calculates the optimal number of iterations for Grover's algorithm, which is approximately `(π/4) * sqrt(N)`, where `N` is the size of the search space. It then constructs and executes the quantum circuit, and the final measurement results are analyzed to identify the solution state.

## How to Run
```bash
python 24_bit_cuda_grovers.py
```
The script will print the configuration of the search, including the number of qubits, the size of the search space, and the optimal number of iterations. It will then display the top 5 measurement results, highlighting the solution state and its probability.
