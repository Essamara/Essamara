# 4-Control CNOT Test (`working8bit4cnot.py`)

This script tests the implementation of a 4-control CNOT (Controlled-NOT) gate using the CUDA-Q framework.

## Description

This script focuses on a specific and complex quantum gate: a CNOT gate that is controlled by four separate qubits. This gate, also known as a multi-controlled Toffoli gate or a 4-controlled X gate, will flip the state of a target qubit if and only if all four of its control qubits are in the `|1>` state.

Such multi-controlled gates are fundamental building blocks for many advanced quantum algorithms, including those used in quantum arithmetic, error correction, and oracle construction for search algorithms. This script serves as a direct test to verify that the CUDA-Q compiler and simulator can correctly handle the syntax and execution of such a gate.

## How It Works

1.  **Qubit Allocation**: The script allocates a 16-qubit register, but only uses the first 5 for this specific test.
2.  **State Preparation**: The first four qubits (`q[0]` to `q[3]`) are designated as the control qubits and are all initialized to the `|1>` state by applying an X gate. The fifth qubit (`q[4]`) is the target qubit and remains in its initial `|0>` state.
3.  **4-Control CNOT Operation**: A single X gate is applied to the target qubit, with all four control qubits passed as arguments to the `.ctrl()` modifier.
4.  **Measurement**: All five qubits involved in the test are measured.

Since all four control qubits are in the `|1>` state, the expected outcome is that the target qubit will be flipped from `|0>` to `|1>`. Therefore, the final measured state of the five qubits should be `11111`.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working8bit4cnot.py
```
The script will execute the quantum circuit and print the most probable measured state. It will then explicitly state whether the outcome matches the expected `11111` state, providing a clear "SUCCESS" or "FAILURE" message for the test. This serves as a validation of the multi-control gate functionality.
