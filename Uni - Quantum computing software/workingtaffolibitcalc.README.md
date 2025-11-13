# Quantum Full Adder (`workingtaffolibitcalc.py`)

This script implements the sum bit of a classical full adder using a quantum circuit.

## Description

A full adder is a fundamental digital logic circuit that adds three single-bit binary numbers (A, B, and a carry-in, C_in) and outputs a two-bit result: a sum bit and a carry-out bit. This script focuses on calculating the **sum bit**, which is determined by the XOR of the three inputs: `Sum = A XOR B XOR C_in`.

The script demonstrates how this classical logic can be directly translated into a quantum circuit using CNOT (Controlled-NOT) gates, as the CNOT gate is the quantum equivalent of the classical XOR gate.

## How It Works

The `full_adder_kernel` defines the quantum circuit:
1.  **Qubit Allocation and Initialization**: Three qubits (`a_qubit`, `b_qubit`, `cin_qubit`) are allocated and initialized to the classical input values (`0` or `1`).
2.  **Quantum XOR Operations**:
    -   A CNOT gate is applied with `b_qubit` as the control and `a_qubit` as the target, effectively calculating `A XOR B` and storing the result in `a_qubit`.
    -   Another CNOT gate is applied with `cin_qubit` as the control and `a_qubit` as the target. This completes the full XOR operation: `(A XOR B) XOR C_in`.
3.  **Measurement**: The `a_qubit`, which now holds the final sum, is measured.

The script then runs a test case for the inputs `A=1`, `B=0`, and `C_in=0`. It compares the measured quantum result to the classically expected sum and reports whether the computation was successful.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python workingtaffolibitcalc.py
```
The script will execute the test case `1 + 0 + 0` and print the result. It will show the measured sum from the quantum circuit and explicitly state "SUCCESS" if it matches the expected sum of `1`, or "FAILURE" otherwise. This provides a clear verification of the quantum full adder's sum logic.
