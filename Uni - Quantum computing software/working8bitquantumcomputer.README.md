# 8-Bit Quantum XOR Sum (`working8bitquantumcomputer.py`)

This script implements an interactive 8-bit quantum calculator that computes the bitwise XOR sum of two numbers using a quantum circuit.

## Description

This script provides a practical demonstration of how a quantum computer can perform a classical logic operation—in this case, the XOR sum. It takes two 8-bit numbers as input from the user, encodes them into the initial state of a 16-qubit register, and then uses a series of CNOT gates to compute the XOR sum.

The script is a clear example of mapping a classical algorithm onto a quantum circuit. It showcases how the fundamental CNOT gate in quantum computing is the direct equivalent of the classical XOR gate.

## How It Works

1.  **User Input**: The script prompts the user to enter two decimal numbers between 0 and 255.
2.  **State Preparation**: The two input numbers are converted into their 8-bit binary representations. A 16-qubit register is then prepared, with the first 8 qubits representing the first number (A) and the second 8 qubits representing the second number (B).
3.  **Quantum XOR Operation**: A CNOT gate is applied to each pair of corresponding qubits from the two registers (A_i and B_i). The qubit from register A acts as the control, and the qubit from register B is the target. This operation effectively computes the bitwise XOR and stores the result in register B.
4.  **Measurement**: The qubits in register B are measured to obtain the final result of the XOR operation.
5.  **Result Display**: The measured binary result is converted back to a decimal number and displayed to the user, along with a comparison to the classically calculated expected result.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working8bitquantumcomputer.py
```
The script will start an interactive prompt. Enter two numbers between 0 and 255 when prompted. The script will then:
- Print the classical expectation for the XOR sum.
- Execute the quantum circuit.
- Display the measured quantum result in both binary and decimal formats.
- Provide a "SUCCESS" or "FAILURE" message indicating whether the quantum computation matched the classical result.
