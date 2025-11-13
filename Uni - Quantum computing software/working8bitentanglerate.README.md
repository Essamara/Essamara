# 16-Qubit Entanglement Throughput Test (`working8bitentanglerate.py`)

This script benchmarks the performance of the 16-qubit quantum entanglement circuit, measuring the rate at which a simulator can execute the full entanglement and measurement process.

## Description

Building on the `working8bitentangle.py` script, this program is designed to quantify the performance of a quantum simulator. Instead of analyzing the quantum state itself, it focuses on the **throughput**: the number of entanglement operations that can be performed per second.

This is a valuable metric for assessing the efficiency of a quantum computing simulator or hardware backend. It provides a clear measure of how quickly the system can execute a moderately complex quantum circuit involving both single-qubit (Hadamard) and multi-qubit (CNOT) gates.

## How It Works

1.  **Define the Entangler Kernel**: The script uses the same `entangler_kernel` as in the previous entanglement script to create eight Bell pairs.
2.  **Repeated Execution**: It runs this kernel in a loop for a specified number of operations (5,000 by default).
3.  **Time Measurement**: The script records the total time taken to complete all the operations.
4.  **Throughput Calculation**: The total number of operations is divided by the total time to calculate the throughput rate in operations per second.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python working8bitentanglerate.py
```
The script will execute the throughput test and then print a summary of the results. The output will include the total number of operations performed, the total time elapsed, and the final calculated throughput rate. This provides a straightforward benchmark of the simulator's performance on this specific quantum task.
