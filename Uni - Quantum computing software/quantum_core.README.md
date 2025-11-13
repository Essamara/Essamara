# Quantum Core API (`quantum_core.py`)

This script serves as the central API for the quantum computing software, providing a translation layer that converts classical-style commands into quantum operations executed using the CUDA-Q framework.

## Description

The `quantum_core.py` script acts as a "Wine" layer, simulating a high-level interface to a quantum processor. It interprets simple string commands and maps them to complex quantum circuits for execution on a simulated or hardware-based quantum target.

The primary functionalities demonstrated are:
1.  **Quantum Teleportation**: Securely transferring a quantum state using an entangled pair of qubits.
2.  **Quantum Search**: Finding a target item in an unstructured database exponentially faster than classical algorithms using Grover's search.
3.  **Single-Qubit Operations**: Applying fundamental quantum gates to a single qubit and measuring the outcome in different bases.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.
- **NumPy**: For numerical operations.
- `bell_state.py`: A required local module that implements the quantum teleportation protocol.
- `quantum_search.py`: A required local module that implements the Grover's search algorithm.

## Available Commands

The script's `classical_command_to_quantum` function accepts the following commands:

### 1. `transfer`
Initiates the quantum teleportation protocol to transfer a predefined quantum state.

- **Usage**: `transfer`
- **Output**: Reports the success or failure of the teleportation by comparing the Z expectation value of the initial and teleported states.

### 2. `search`
Executes Grover's search algorithm to find a target state ('11') in a 2-qubit search space.

- **Usage**: `search`
- **Output**: Reports whether the target was found with high probability, demonstrating the speed-up of quantum search.

### 3. `qubit_op`
Performs a single-qubit operation with a specified initial state, gate, and measurement basis.

- **Usage**: `qubit_op [GATE] [INITIAL_STATE] [MEASUREMENT_BASIS]`
- **Arguments**:
  - `GATE`: The quantum gate to apply (`X`, `S`, or `H`).
  - `INITIAL_STATE`: The starting state of the qubit (`0` or `1`).
  - `MEASUREMENT_BASIS`: The basis to measure in (`X`, `Y`, or `Z`).
- **Example**: `qubit_op H 0 X` (Apply a Hadamard gate to a qubit in state |0> and measure in the X basis).
- **Output**: Provides a detailed breakdown of the measurement results, including state counts and probabilities.

## How to Run

The script can be run directly to execute a test of the `qubit_op` command:
```bash
python quantum_core.py
```
To use its functionality within another application, import the `classical_command_to_quantum` function.
