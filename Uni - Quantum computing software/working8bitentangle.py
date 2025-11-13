import cudaq
import sys

sys.setrecursionlimit(5000)

NUM_BITS = 8
TOTAL_QUBITS = 2 * NUM_BITS

# ----------------------------------------------------
# 1. Quantum Kernel Definition: 8-Bit Entangler (UNCHANGED)
# ----------------------------------------------------
@cudaq.kernel
def entangler_kernel():
    """
    Creates 8 maximally entangled Bell pairs between the 16 qubits.
    Register A (q[0:7]) and Register B (q[8:15]) are entangled.
    """
    q = cudaq.qvector(TOTAL_QUBITS)

    # 1. Apply Hadamard to Register A (q[0] to q[7])
    for i in range(NUM_BITS):
        h(q[i])

    # 2. Apply CNOTs to entangle A and B
    for i in range(NUM_BITS):
        cx(q[i], q[i + NUM_BITS])

    # 3. Measurement (Measure ALL 16 qubits)
    mz(q)

# ----------------------------------------------------
# 2. Driver Logic: Run and Analyze Distribution
# ----------------------------------------------------

def run_entanglement_test():

    print(f"\n--- 16-Qubit Entanglement Test ({NUM_BITS} Bell Pairs) ---")
    print(f"Running circuit once to get the full probability distribution.")
    print("-" * 50)

    # Run the kernel ONCE without 'shots' to get the full probability distribution
    # The result contains a dictionary of {state_string: probability}
    result = cudaq.sample(entangler_kernel)

    # Analyze the results
    total_correlated_probability = 0.0
    uncorrelated_states = {}

    # Iterate over all measured states and their probabilities
    for state, probability in result.items():
        # state is a 16-bit string (e.g., '0110011001100110')

        # Split the 16-bit string into A (first 8) and B (last 8)
        A_reg = state[:NUM_BITS]
        B_reg = state[NUM_BITS:]

        # Check the fundamental property of Bell pairs: A must equal B
        if A_reg == B_reg:
            total_correlated_probability += probability
        else:
            if probability > 1e-9: # Only track non-negligible errors
                uncorrelated_states[state] = probability

    # Output the analysis
    print(f"Total States in Distribution: {len(result)}")
    print(f"Total Correlated Probability (A == B): {total_correlated_probability:.6f}")
    print(f"Total Uncorrelated Probability (A != B): {1.0 - total_correlated_probability:.6f}")
    print("-" * 50)

    # The rate is the percentage of probability space that shows perfect correlation
    correlation_rate = total_correlated_probability * 100

    print(f"Entanglement Correlation Rate: **{correlation_rate:.2f}%**")

    # Show the two most likely states (which should be correlated)
    sorted_results = sorted(result.items(), key=lambda item: item[1], reverse=True)

    print("\nTop 5 Measured States and Their Probabilities:")
    for state, prob in sorted_results[:5]:
        A_reg = state[:NUM_BITS]
        B_reg = state[NUM_BITS:]

        status = "✅ Correlated (A=B)" if A_reg == B_reg else "❌ Uncorrelated"

        print(f"  A: {A_reg} | B: {B_reg} | Prob: {prob:.4f} {status}")

    if uncorrelated_states:
        print("\n⚠️ Warning: The simulator should not show uncorrelated states with significant probability.")
        print(f"  Number of Uncorrelated States: {len(uncorrelated_states)}")

if __name__ == "__main__":
    run_entanglement_test()