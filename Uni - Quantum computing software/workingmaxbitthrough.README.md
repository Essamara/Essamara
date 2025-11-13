# 5-Bit Parallel CCNOT Throughput Test (`workingmaxbitthrough.py`)

This script is a benchmark designed to stress-test a quantum simulator by measuring the throughput of a 5-bit parallel CCNOT (Toffoli) gate operation, utilizing 15 out of 16 available qubits.

## Description

This script pushes the boundaries of the simulator's capacity by implementing a complex parallel quantum computation. It simulates five simultaneous 3-qubit Toffoli gates, which is equivalent to performing a bitwise AND operation on two 5-bit numbers.

The primary goal of this script is to measure performance under a heavy load. It generates a large number of random 5-bit inputs, executes the parallel quantum computation for each, and calculates the overall throughput in operations per second. This provides a valuable benchmark for the simulator's ability to handle complex, multi-qubit circuits.

## How It Works

1.  **Random Data Generation**: The script creates a large dataset of random pairs of 5-bit numbers (`A` and `B`) and pre-calculates the expected result of a classical bitwise AND operation.
2.  **Quantum Kernel Execution**: For each pair of numbers, the `parallel_ccnot_kernel` is executed.
    -   It initializes two 5-qubit registers to the states of `A` and `B`.
    -   It applies five CCNOT gates in parallel, with the qubits from `A` and `B` as controls and a third 5-qubit register (`C`) as the target.
    -   It measures the target register `C` to get the result.
3.  **Verification**: The measured quantum result is compared against the pre-calculated classical result to ensure accuracy.
4.  **Time Measurement and Throughput Calculation**: The total time taken to execute all the quantum operations is recorded, and this is used to calculate the final throughput rate.

## Dependencies

- **Python 3.x**
- **CUDA-Q**: The quantum computing platform from NVIDIA.

## How to Run
```bash
python workingmaxbitthrough.py
```
The script will run the benchmark, executing 5,000 parallel CCNOT operations by default. After the test is complete, it will print a detailed summary including:
- The total number of operations performed.
- The total time elapsed.
- The verification success rate (which should be 100%).
- The final throughput rate in operations per second.

This provides a clear and demanding benchmark of the simulator's performance on a near-maximum capacity quantum circuit.
