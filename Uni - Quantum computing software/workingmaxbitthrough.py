import cudaq
import sys
import time
import random

sys.setrecursionlimit(5000)

# MAXING OUT THE SIMULATOR
NUM_BITS = 5 # 5-bit logic
TOTAL_QUBITS_FOR_TEST = 3 * NUM_BITS # 15 qubits: 5 controls A, 5 controls B, 5 targets C
TOTAL_QUBITS_OVERALL = 16 # Your full available capacity

# Max input value (31)
MAX_VALUE = 2**NUM_BITS - 1
NUM_OPERATIONS = 5000 # Runs for the throughput test

# ----------------------------------------------------
# 1. Quantum Kernel Definition: 5-Bit Parallel CCNOT
# ----------------------------------------------------
@cudaq.kernel
def parallel_ccnot_kernel(input_a: list[int], input_b: list[int]):
    """
    Performs 5 simultaneous CCNOT (Toffoli) operations across 15 qubits.
    q[0:4] (A), q[5:9] (B) control q[10:14] (C).
    """
    # Note: We use 16 total qubits, but only the first 15 are involved.
    q = cudaq.qvector(TOTAL_QUBITS_OVERALL)

    # 1. State Preparation: Initialize A and B based on input lists
    # Initialize A (q[0] to q[4])
    for i in range(NUM_BITS):
        if input_a[i] == 1:
            x(q[i])

    # Initialize B (q[5] to q[9])
    for i in range(NUM_BITS):
        if input_b[i] == 1:
            x(q[i + NUM_BITS])

    # 2. Parallel CCNOT Array: Run 5 CCNOTs in parallel
    for i in range(NUM_BITS):
        control_A = q[i]
        control_B = q[i + NUM_BITS]
        target_C = q[i + 2 * NUM_BITS] # q[10] to q[14]

        # Use the working manual syntax for a 3-qubit CCNOT
        x.ctrl(control_A, control_B, target_C)

    # 3. Measurement: Measure the 5-bit Output Register (C)
    mz(q[10:15])

# ----------------------------------------------------
# 2. Helper Functions and Driver Logic
# ----------------------------------------------------

def to_bit_list(value):
    """Converts a decimal 0-31 to a 5-element LSB-first list."""
    return [int(bit) for bit in format(value, f'0{NUM_BITS}b')][::-1]

def run_throughput_test():

    print(f"\n--- MAXED OUT: {NUM_BITS}-Bit Parallel CCNOT Throughput Test (15 Qubits) ---")
    print(f"Simulating {NUM_BITS} parallel AND gates (Max Number: {MAX_VALUE}).")
    print(f"Executing {NUM_OPERATIONS:,} runs on the CUDA-Q simulator.")
    print("-" * 65)

    # --- Generate Random Inputs and Expected Results ---
    test_data = []
    for _ in range(NUM_OPERATIONS):
        A = random.randint(0, MAX_VALUE)
        B = random.randint(0, MAX_VALUE)

        # Classical 5-bit AND operation for verification
        expected_output = A & B

        test_data.append({
            'A_bits': to_bit_list(A),
            'B_bits': to_bit_list(B),
            'expected': format(expected_output, f'0{NUM_BITS}b') # MSB first string for comparison
        })

    # --- Run Test and Measure Time ---
    start_time = time.time()
    success_count = 0

    for data in test_data:
        result = cudaq.sample(parallel_ccnot_kernel, data['A_bits'], data['B_bits'])

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
    run_throughput_test()