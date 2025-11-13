import cudaq
import sys
import time
import random

sys.setrecursionlimit(5000)

NUM_BITS = 16 # We use all 16 available qubits
TOTAL_QUBITS_OVERALL = 16 # All qubits are used for the single 16-bit register

# Max input value (65535)
MAX_VALUE = 2**NUM_BITS - 1
NUM_OPERATIONS = 10000 # Increase runs for a better benchmark

# ----------------------------------------------------
# 1. Quantum Kernel Definition: 16-Bit Parallel NOT
# ----------------------------------------------------
@cudaq.kernel
def parallel_not_kernel(input_state: list[int]):
    """
    Performs 16 simultaneous NOT (X) operations across all 16 qubits.
    """
    q = cudaq.qvector(TOTAL_QUBITS_OVERALL)

    # 1. State Preparation: Initialize the 16-bit register
    for i in range(NUM_BITS):
        if input_state[i] == 1:
            x(q[i])

    # 2. 16-Bit NOT Operation: Apply X gate to every qubit in parallel
    for i in range(NUM_BITS):
        x(q[i])

    # 3. Measurement: Measure the entire 16-bit register
    mz(q)

# ----------------------------------------------------
# 2. Helper Functions and Driver Logic
# ----------------------------------------------------

def to_bit_list(value):
    """Converts a decimal 0-65535 to a 16-element LSB-first list."""
    return [int(bit) for bit in format(value, f'0{NUM_BITS}b')][::-1]

def run_16bit_throughput_test():

    print(f"\n--- 16-Bit Parallel NOT Throughput Test (16 Qubits) ---")
    print(f"Max Number Handled: {MAX_VALUE:,}")
    print(f"Executing {NUM_OPERATIONS:,} runs on the CUDA-Q simulator.")
    print("-" * 65)

    # --- Generate Random Inputs and Expected Results ---
    test_data = []
    for _ in range(NUM_OPERATIONS):
        A = random.randint(0, MAX_VALUE)

        # Classical 16-bit NOT operation for verification (XOR with all 1s)
        expected_output = A ^ MAX_VALUE

        test_data.append({
            'A_bits': to_bit_list(A),
            'expected': format(expected_output, f'0{NUM_BITS}b') # MSB first string
        })

    # --- Run Test and Measure Time ---
    start_time = time.time()
    success_count = 0

    for data in test_data:
        # Pass only the input state
        result = cudaq.sample(parallel_not_kernel, data['A_bits'])

        measured_state_reversed = result.most_probable() # LSB first string
        measured_state = measured_state_reversed[::-1] # MSB first for comparison

        if measured_state == data['expected']:
            success_count += 1

    end_time = time.time()
    total_time = end_time - start_time

    # --- Calculate Throughput ---
    if total_time > 0:
        throughput_rate = NUM_OPERATIONS / total_time
    else:
        throughput_rate = float('inf')

    # --- Output Results ---
    print(f"Total Operations Executed: {NUM_OPERATIONS:,}")
    print(f"Total Time Elapsed:        {total_time:.4f} seconds")
    print(f"Verification Success Rate: {(success_count/NUM_OPERATIONS)*100:.2f}%")
    print("-" * 65)
    print(f"Throughput Rate: **{throughput_rate:,.2f} operations/second**")
    print("-" * 65)

if __name__ == "__main__":
    run_16bit_throughput_test()