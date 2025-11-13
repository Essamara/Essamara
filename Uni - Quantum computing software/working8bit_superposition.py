import cudaq
import sys
from collections import Counter

# Setting a high recursion limit for good measure
sys.setrecursionlimit(5000)

NUM_BITS = 8
TOTAL_QUBITS = 2 * NUM_BITS

# ----------------------------------------------------
# 1. Quantum Kernel Definition
# ----------------------------------------------------
@cudaq.kernel
def superposition_kernel(x_init_data: list[int]):
    """
    Implements the 8-bit XOR sum with one control qubit (q[0]) in superposition.
    """
    q = cudaq.qvector(TOTAL_QUBITS)

    # --- State Preparation (Initialize inputs) ---
    for i in range(NUM_BITS):
        if x_init_data[NUM_BITS - 1 - i] == 1:
            x(q[i])

    for i in range(NUM_BITS):
        if x_init_data[TOTAL_QUBITS - 1 - i] == 1:
            x(q[i + NUM_BITS])

    # --- SUPERPOSITION STEP ---
    # Put A's LSB (q[0]) into equal superposition.
    h(q[0])

    # --- XOR Sum Logic (A XOR B) ---
    cx(q[0], q[8])
    cx(q[1], q[9])
    cx(q[2], q[10])
    cx(q[3], q[11])
    cx(q[4], q[12])
    cx(q[5], q[13])
    cx(q[6], q[14])
    cx(q[7], q[15])

    # --- Measurement ---
    mz(q[8:])


# ----------------------------------------------------
# 2. Interactive Driver Logic
# ----------------------------------------------------

def run_superposition_test():

    A_val = 4
    B_val = 5

    # Classical Logic:
    A_bits = [int(bit) for bit in format(A_val, f'0{NUM_BITS}b')]
    B_bits = [int(bit) for bit in format(B_val, f'0{NUM_BITS}b')]

    x_init_data = A_bits + B_bits

    print("\n--- 8-Bit Quantum Superposition Test ---")
    print(f"Classical Input A: {A_val} (LSB is forced into superposition)")
    print(f"Classical Input B: {B_val}")
    print("\nExpected Outputs (50% each):")
    print(f"  Result 1 (4 XOR 5): 1")
    print(f"  Result 2 (5 XOR 5): 0")
    print("-" * 40)

    try:
        # Sample the kernel (assuming default number of shots is used)
        result = cudaq.sample(superposition_kernel, x_init_data)

        # FIX: The SampleResult object is now treated as the dictionary of counts itself.
        # This works if the SampleResult object implements the dictionary interface.
        total_shots = sum(result.values())

        # Convert bit strings to decimals for display
        decimal_counts = Counter()
        for bit_string, count in result.items():
            # Reverse for MSB-first conversion
            decimal_val = int(bit_string[::-1], 2)
            decimal_counts[decimal_val] += count

        print("Quantum Measurement Results:")
        for dec_val, count in sorted(decimal_counts.items()):
            probability = count / total_shots * 100
            print(f"  Result {dec_val}: {count} shots ({probability:.1f}%)")

        print("-" * 40)
        # Check if both expected results are present (within tolerance)
        if 0 in decimal_counts and 1 in decimal_counts and len(decimal_counts) == 2:
            print("STATUS: SUCCESS ✅ - Quantum superposition demonstrated.")
        else:
            print("STATUS: FAILURE ❌ - Results were unexpected. (Expected results 0 and 1)")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_superposition_test()