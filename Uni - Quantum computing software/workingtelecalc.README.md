# Quantum Teleportation (`workingtelecalc.py`)

This script provides a clear demonstration of the quantum teleportation protocol, a process that allows the state of a qubit to be transmitted from one location to another without physically moving the qubit itself.

## Description

Quantum teleportation is a foundational protocol in quantum communication and distributed quantum computing. It relies on the principles of entanglement and classical communication to "teleport" a quantum state. This script implements the full protocol to teleport the state `|1>` from a source qubit (A) to a destination qubit (C).

## How It Works

The teleportation protocol is executed in the `teleportation_kernel` and involves three qubits and several key steps:

1.  **State Preparation**:
    -   The source qubit (A) is prepared in the state `|1>`, which is the state we want to teleport.
    -   An entangled Bell pair is created between the other two qubits, B and C. This entangled pair acts as the quantum channel for the teleportation.

2.  **Bell State Measurement**:
    -   The sender (Alice) performs a joint measurement, known as a Bell state measurement, on her two qubits: the source qubit (A) and her half of the entangled pair (B). This measurement extracts two classical bits of information.

3.  **Classical Communication**:
    -   The two classical bits from Alice's measurement are sent to the receiver (Bob) through a classical communication channel.

4.  **State Reconstruction**:
    -   Based on the two classical bits he receives, Bob applies a specific set of correction gates (an X gate and/or a Z gate) to his half of the entangled pair (qubit C).

After these correction gates are applied, qubit C will be in the exact same state as the original source qubit A, and the teleportation is complete.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python workingtelecalc.py
```
The script will run the full teleportation protocol. It initializes qubit A to the state `|1>` and then checks the final state of qubit C. It will print:
- The final measured state of the destination qubit C.
- A "SUCCESS" message if the state of C is `|1>`, confirming that the teleportation was successful.
- A "FAILURE" message if the state is incorrect.
