import cudaq
import sys

sys.setrecursionlimit(5000)

NUM_BITS = 4
TOTAL_QUBITS_FOR_TEST = 3 * NUM_BITS # 12 qubits: 4 controls A, 4 controls B, 4 targets C
TOTAL_QUBITS_OVERALL = 16

# ----------------------------------------------------
# 1. Quantum Kernel Definition: 4-Bit Parallel CCNOT
# ----------------------------------------------------
@cudaq.kernel
def parallel_ccnot_kernel():
    """
    Performs 4 simultaneous CCNOT (Toffoli) operations across 12 qubits.
    q[0:3] (A) and q[4:7] (B) control q[8:11] (C).
    """
    q = cudaq.qvector(TOTAL_QUBITS_OVERALL)

    # 1. State Preparation: Set ALL 8 Control qubits (A and B) to |1>
    # q[0] through q[7] are set to |1>
    for i in range(2 * NUM_BITS):
        x(q[i])

    # 2. Parallel CCNOT Array: Run 4 CCNOTs in parallel
    # NOTE: Removed the 'print' statement to fix the CompilerError
    for i in range(NUM_BITS):

        # Define the indices for the i-th parallel gate:
        control_A = q[i]
        control_B = q[i + NUM_BITS]
        target_C = q[i + 2 * NUM_BITS]

        # Use the working manual syntax for a 3-qubit CCNOT
        x.ctrl(control_A, control_B, target_C)

    # 3. Measurement: Measure the 4-bit Output Register (C)
    # The output register is q[8] to q[11]
    mz(q[8:12])

# ----------------------------------------------------
# 2. Driver Logic
# ----------------------------------------------------

def run_parallel_ccnot_test():

    print(f"\n--- {NUM_BITS}-Bit Parallel CCNOT Array Test (12 Qubits) ---")
    print("Simulating the quantum equivalent of 4 parallel AND gates: (1 AND 1) x 4.")
    print("-" * 65)

    # Run the kernel once to get the exact result distribution
    result = cudaq.sample(parallel_ccnot_kernel)
    most_probable_state = result.most_probable()

    # Expected state: 4 output bits should all flip to |1> -> "1111"
    expected_state = "1" * NUM_BITS

    print(f"Most Probable Measured State (Output Register C): {most_probable_state}")

    if most_probable_state == expected_state:
        print(f"STATUS: SUCCESS ✅ - **4-Bit Parallel Logic** confirmed. Output: **{expected_state}**.")
    else:
        print("STATUS: FAILURE ❌ - Check circuit logic.")

if __name__ == "__main__":
    run_parallel_ccnot_test()