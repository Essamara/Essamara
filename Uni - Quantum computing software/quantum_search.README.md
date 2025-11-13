# Grover's Quantum Search (`quantum_search.py`)

This script provides an implementation of Grover's search algorithm for a 2-qubit system using the CUDA-Q framework.

## Description

Grover's algorithm is a quantum search algorithm that can find a specific item in an unsorted database with a quadratic speed-up over the best possible classical algorithm. This implementation is specifically designed for a 2-qubit system, which has a search space of four possible states: `00`, `01`, `10`, and `11`.

The script is structured into three main components:
1.  **The Oracle (`apply_oracle`)**: A function that marks the target quantum state by inverting its phase.
2.  **The Diffuser (`apply_diffuser`)**: A function that amplifies the amplitude of the marked state, increasing its measurement probability.
3.  **The Main Function (`grover_search`)**: A function that orchestrates the search by initializing the qubits, applying the oracle and diffuser for a specified number of iterations, and measuring the final state.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.
- **NumPy**: For numerical operations.

## How It Works

The `grover_search` function performs the following steps:

1.  **Initialization**: Prepares the qubits in a uniform superposition of all possible states using Hadamard gates.
2.  **Iteration**: Repeatedly applies the oracle and the diffuser.
    - The **oracle** flips the sign of the target state.
    - The **diffuser** (also known as amplification) reflects the states about the average amplitude, which increases the amplitude of the target state.
3.  **Measurement**: Measures the qubits after the iterations are complete. The state with the highest probability is the result of the search.

## Usage

To use the search functionality, import the `grover_search` function and provide the necessary arguments.

- **Function Signature**: `grover_search(n_qubits: int, iterations: int, target_state: str, shots_count: int)`
- **Arguments**:
  - `n_qubits`: The number of qubits (currently fixed at 2).
  - `iterations`: The number of times to apply the oracle and diffuser. For a 2-qubit system, one iteration is optimal.
  - `target_state`: The binary string representing the state to search for (e.g., `'11'`).
  - `shots_count`: The number of times to run the quantum circuit to gather statistics.

- **Returns**: A dictionary containing the measurement results, the most likely state found, and the success rate.

### Example

```python
from quantum_search import grover_search

# Search for the state '11'
results = grover_search(n_qubits=2, iterations=1, target_state='11', shots_count=1000)

print(f"Target found: {results['most_likely']}")
print(f"Success rate: {results['success_rate']:.2f}%")
```

This script is designed to be used as a module by `quantum_core.py` but can also be tested independently.
