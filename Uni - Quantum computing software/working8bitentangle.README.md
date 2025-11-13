# 8-Bit Quantum Entanglement (`working8bitentangle.py`)

This script demonstrates the creation of eight maximally entangled Bell pairs using the CUDA-Q framework.

## Description

This script showcases one of the most counter-intuitive and powerful phenomena in quantum mechanics: entanglement. It creates eight pairs of entangled qubits, where the state of each qubit in a pair is perfectly correlated with the state of the other, regardless of the distance separating them.

The script uses a standard quantum circuit to generate these Bell pairs. When the qubits are measured, the two qubits in each pair will always yield the same result—either both are `0` or both are `1`. This perfect correlation is a hallmark of entanglement.

## How It Works

1.  **Qubit Allocation**: The script allocates a 16-qubit register, divided into two 8-qubit sub-registers, A and B.
2.  **Superposition**: A Hadamard gate is applied to each qubit in register A, putting them all into a superposition of `|0>` and `|1>`.
3.  **Entanglement**: A CNOT gate is applied to each of the eight pairs of qubits, with the qubit from register A as the control and the corresponding qubit from register B as the target. This operation entangles each pair.
4.  **Measurement**: All 16 qubits are measured.

The script then analyzes the measurement results to verify the entanglement. It calculates the "Entanglement Correlation Rate," which is the percentage of measurements where the state of register A is identical to the state of register B. For a perfect simulation of entanglement, this rate should be 100%.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working8bitentangle.py
```
The script will execute the entanglement circuit and print a detailed analysis of the results. It will show the total probability of correlated vs. uncorrelated states and display the top 5 most measured states, indicating whether they are correlated. The final output is the Entanglement Correlation Rate, which should be very close to 100%, providing a clear demonstration of successful entanglement.
