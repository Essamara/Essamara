# Quantum Teleportation (`bell_state.py`)

This script implements the quantum teleportation protocol using the CUDA-Q framework. It demonstrates how to transfer a quantum state from one location to another without physically moving the qubit.

## Description

Quantum teleportation is a process by which the exact state of a quantum system can be transmitted from one location to another, with the help of classical communication and a pre-shared entangled state. This script teleports the state of a "message" qubit (Q0) from a sender (Alice) to a receiver (Bob).

The protocol is implemented in the `teleport_quantum_state` function and follows these key steps:

1.  **Entanglement**: A Bell pair (an entangled pair of qubits) is created and shared between Alice (Q1) and Bob (Q2).
2.  **State Preparation**: The message qubit (Q0) is prepared in a specific quantum state determined by an input angle.
3.  **Bell Measurement**: Alice performs a joint measurement on her two qubits (the message qubit Q0 and her half of the entangled pair Q1).
4.  **Classical Communication**: The results of Alice's measurement (two classical bits) are sent to Bob.
5.  **State Reconstruction**: Based on the classical bits he receives, Bob applies a specific set of correction gates (Pauli X and Z gates) to his half of the entangled pair (Q2).

After these steps, Bob's qubit (Q2) will be in the exact same state as the original message qubit (Q0).

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.
- **NumPy**: For numerical operations.

## Usage

The primary function `teleport_quantum_state` can be imported and used to simulate the teleportation process.

- **Function Signature**: `teleport_quantum_state(message_angle: float)`
- **Arguments**:
  - `message_angle`: The angle (in radians) used in an RY gate to prepare the initial state of the message qubit.
- **Returns**: The Z expectation value (`<Z>`) of the teleported qubit (Bob's qubit), which can be used to verify if the teleportation was successful.

### Example

```python
import numpy as np
from bell_state import teleport_quantum_state

# The angle to prepare the initial state
angle = np.pi / 4

# Calculate the expected <Z> value
initial_z_exp = np.cos(angle)

# Run the teleportation
teleported_z_exp = teleport_quantum_state(angle)

# Check if the teleported state matches the original
print(f"Initial <Z>: {initial_z_exp:.4f}")
print(f"Teleported <Z>: {teleported_z_exp:.4f}")
print(f"Error: {abs(initial_z_exp - teleported_z_exp):.4f}")
```

The script includes a self-test block (`if __name__ == '__main__':`) that runs this example when the file is executed directly.
