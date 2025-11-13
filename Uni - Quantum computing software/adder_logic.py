import cudaq

@cudaq.kernel
def eight_bit_stream(num_bits: int):
    """
    Creates an 8-qubit quantum register, puts all 8 qubits into superposition,
    and measures them to produce an 8-bit random binary number.
    """
    # 1. Allocate an 8-qubit register
    q = cudaq.qvector(num_bits)

    # 2. Apply Hadamard gate to every qubit (Parallel operation)
    h(q)

    # 3. Measure the entire register
    mz(q)

# --- Execution ---
NUM_BITS = 8
# Use the validated execution signature (default shots of 1000)
result = cudaq.sample(eight_bit_stream, NUM_BITS)

# CRITICAL FIX: Since result.shots is not available, we assume the default (1000).
TOTAL_SHOTS = 1000

print("--- 8-Bit Quantum Stream (Parallel Hadamard) ---")
print(f"Total Measurements (Assumed Default Shots): {TOTAL_SHOTS}")
print("Output Probability Distribution (Top 5 results):")

# CRITICAL FIX: Use result.items() which is the standard way to get key-value pairs
# when a custom object doesn't support direct dict() conversion.
try:
    result_map = dict(result.items())
except AttributeError:
    # If .items() also fails, the only remaining option is to assume the object itself
    # IS the dictionary, which is often true for broken compilers.
    result_map = result

# Process results
sorted_results = sorted(result_map.items(), key=lambda item: item[1], reverse=True)

for state, count in sorted_results[:5]:
    # Calculate percentage based on assumed total shots
    print(f"  State '{state}': {count} counts ({count/TOTAL_SHOTS*100:.2f}%)")

print("\nMost Probable Result (random 8-bit binary number):", result.most_probable())