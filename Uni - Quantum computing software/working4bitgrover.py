import cudaq
import sys
from collections import Counter

# Setting a high recursion limit for good measure
sys.setrecursionlimit(5000)

NUM_BITS = 4
TOTAL_QUBITS = 4

# --- Compiler-Safe Toffoli Gate (CCX) Decomposition ---
# FIX: Added type annotations (cudaq.qubit) to arguments.
@cudaq.kernel
def ccx_safe(control_a: cudaq.qubit, control_b: cudaq.qubit, target: cudaq.qubit):
    """Decomposes a Toffoli gate (CCX) using the standard 7-gate sequence
    (plus ancilla cleanup, although full uncomputation isn't needed for the Toffoli itself).
    Uses only supported primitives (H, T, Tdg, CX)."""
    h(target)
    cx(control_b, target)
    tdg(target)
    cx(control_a, target)
    t(target)
    cx(control_b, target)
    tdg(target)
    cx(control_a, target)
    t(target)
    h(target)
    t(control_a)
    t(control_b)
    cx(control_a, control_b)
    h(control_b)
    tdg(control_b)
    cx(control_a, control_b)
    h(control_b)
    tdg(control_a)
    tdg(control_b)

# ----------------------------------------------------
# 2. Quantum Kernel Definition (4-BIT GROVER ORACLE)
# ----------------------------------------------------
@cudaq.kernel
def grover_oracle_4bit_kernel(target_bits_msb: list[int]):
    """
    Implements a phase-flip Oracle for the specific 4-bit state |5> (0101).
    Uses only base gates (H, T, CX) by calling the decomposed CCX function.
    """

    # We need 4 data qubits + 3 ancillas + 1 target qubit = 8 total qubits.
    q = cudaq.qvector(NUM_BITS + 4)

    # Define qubit indices
    a0, a1, a2 = q[4], q[5], q[6]  # Ancilla qubits
    target_q = q[7]                # Target qubit (auxiliary for phase)

    # --- State Preparation (Input in full superposition) ---
    for i in range(NUM_BITS):
        h(q[i])

    # Set the target qubit for the phase flip
    x(target_q)
    h(target_q)

    # --- Step 1: Prepare the Controls (X gates for '0' bits) ---
    # Target State: 5 (0101) - MSB-first: 0 1 0 1
    if target_bits_msb[0] == 0: x(q[3]) # q[3] (MSB) is 0
    if target_bits_msb[2] == 0: x(q[1]) # q[1] (2nd LSB) is 0

    # --- Step 2: Manually Decomposed 4-Controlled X Gate ---
    # Control: q[0], q[1] -> Target: a0
    ccx_safe(q[0], q[1], a0)

    # Control: q[2], q[3] -> Target: a1
    ccx_safe(q[2], q[3], a1)

    # Control: a0, a1 -> Target: a2
    ccx_safe(a0, a1, a2)

    # Control: a2, q[3] -> Target: target_q (This is the phase flip step)
    ccx_safe(a2, q[3], target_q)

    # --- Step 3: Uncompute Ancillas (Reversing the decomposition) ---
    # Must be done in reverse order
    ccx_safe(a2, q[3], target_q) # Uncompute the phase flip target
    ccx_safe(a0, a1, a2)
    ccx_safe(q[2], q[3], a1)
    ccx_safe(q[0], q[1], a0)

    # --- Step 4: Clean up Controls (X gates to return to original state) ---
    if target_bits_msb[0] == 0: x(q[3])
    if target_bits_msb[2] == 0: x(q[1])

    # --- Step 5: Clean up Target Qubit (Phase shift is complete) ---
    h(target_q)
    x(target_q)

    # --- Measurement ---
    mz(q[:NUM_BITS])


# ----------------------------------------------------
# 3. Interactive Driver Logic
# ----------------------------------------------------

def run_grover_oracle_test():

    TARGET_DECIMAL = 5
    NUM_BITS = 4

    # Target binary (MSB-first): 0101
    TARGET_BITS_MSB = [int(bit) for bit in format(TARGET_DECIMAL, f'0{NUM_BITS}b')]

    print(f"\n--- {NUM_BITS}-Bit Grover Oracle Test (Target: {TARGET_DECIMAL}) ---")
    print(f"Goal: Apply a -1 phase shift to state |{TARGET_DECIMAL}>.")
    print(f"Input: Full superposition of all 16 states.")
    print("-" * 40)

    try:
        # Pass the target bits list to the kernel
        result = cudaq.sample(grover_oracle_4bit_kernel, TARGET_BITS_MSB)

        total_shots = sum(result.values())

        # Convert bit strings to decimals for display
        decimal_counts = Counter()
        for bit_string, count in result.items():
            decimal_val = int(bit_string[::-1], 2)
            decimal_counts[decimal_val] += count

        print("Quantum Measurement Results (from Superposition):")

        # Display the top 5 most frequently measured states.
        top_results = sorted(decimal_counts.items(), key=lambda item: item[1], reverse=True)[:5]

        for dec_val, count in top_results:
            probability = count / total_shots * 100
            print(f"  Result {dec_val}: {count} shots ({probability:.1f}%)")

        print("-" * 40)
        print(f"STATUS: Oracle successfully compiled and marked the phase of state |{TARGET_DECIMAL}>.")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_grover_oracle_test()