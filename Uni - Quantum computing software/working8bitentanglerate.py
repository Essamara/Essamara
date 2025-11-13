import cudaq
import sys
import time
import random

sys.setrecursionlimit(5000)

NUM_BITS = 8
TOTAL_QUBITS = 2 * NUM_BITS
NUM_OPERATIONS = 5000 # <-- Define the number of runs for the test

# --- Your Entangler Kernel (unchanged) ---
@cudaq.kernel
def entangler_kernel():
    q = cudaq.qvector(TOTAL_QUBITS)
    for i in range(NUM_BITS):
        h(q[i])
    for i in range(NUM_BITS):
        cx(q[i], q[i + NUM_BITS])
    mz(q)
# ------------------------------------------

def run_entanglement_throughput_test():

    print(f"\n--- 16-Qubit Entanglement Throughput Test ---")
    print(f"Executing {NUM_OPERATIONS:,} runs on the CUDA-Q simulator.")
    print("-" * 45)

    # --- Run Test and Measure Time ---
    start_time = time.time()

    # Loop and run the quantum kernel repeatedly
    for _ in range(NUM_OPERATIONS):
        # We only care about the time to execute the quantum part
        result = cudaq.sample(entangler_kernel)
        # Optional: Add minimal verification here if desired, but we skip it for raw speed

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
    print("-" * 45)
    print(f"Throughput Rate: **{throughput_rate:,.2f} operations/second**")
    print("-" * 45)

if __name__ == "__main__":
    run_entanglement_throughput_test()