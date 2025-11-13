# 16-Bit Parallel NOT Throughput Test (`working16bitgood.py`)

This script benchmarks the performance of a 16-bit parallel NOT gate operation using the CUDA-Q framework.

## Description

This script is designed to measure the throughput of a quantum computer simulator by executing a large number of 16-bit parallel NOT operations. A NOT gate (or X gate) is a fundamental quantum gate that flips the state of a qubit from |0> to |1> and vice versa. By applying this gate to all 16 qubits in a register simultaneously, we can perform a bitwise NOT operation on a 16-bit number.

The script performs the following steps:
1.  **Random Data Generation**: It generates a large set of random 16-bit numbers and their expected outputs after a bitwise NOT operation.
2.  **Quantum Kernel Execution**: For each random number, it initializes a 16-qubit register to the corresponding state and then applies an X gate to every qubit in parallel.
3.  **Measurement and Verification**: The final state of the register is measured and compared against the expected output.
4.  **Throughput Calculation**: The total time taken to execute all the operations is measured, and the throughput is calculated in operations per second.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working16bitgood.py
```
The script will run a throughput test with 10,000 operations by default. It will then print a summary of the test, including the total number of operations, the total time elapsed, the success rate of the verification, and the final throughput rate in operations per second. This provides a clear benchmark of the simulator's performance on this specific parallel quantum task.
