import cudaq
import numpy as np

# Define the number of qubits (N) for the search space
NUM_QUBITS = 24
# The number of items in the search space (N)
N_SEARCH = 2**NUM_QUBITS
# The optimal number of iterations for Grover's algorithm
# Optimal iterations = round(pi/4 * sqrt(N/M)) where M=1 solution
NUM_ITERATIONS = int(np.round(np.pi / 4 * np.sqrt(N_SEARCH)))

print(f"CUDA-Q Grover's Search Simulation")
print(f"Number of Qubits: {NUM_QUBITS}")
print(f"Search Space Size (N): {N_SEARCH}")
print(f"Optimal Iterations: {NUM_ITERATIONS}")
print("-" * 35)

# --- 1. The Oracle Kernel (Marks the solution |111...1>) ---
@cudaq.kernel
def grover_oracle(qubits: cudaq.qvector):
    # This oracle flips the phase of the target state |111...1>
    # It requires a multi-controlled Z gate (MCZ) over all qubits.
    # We achieve MCZ by using an X-gate sandwich with a single Z-gate

    # 1. Flip all |0> components to |1> (since the target is |111...1>)
    for i in range(qubits.size()):
        cudaq.x(qubits[i])

    # 2. Apply the multi-controlled Z gate (MCZ)
    # Note: CUDA-Q's default simulator optimizes this high-level MCZ operation.
    cudaq.z.ctrl(qubits)

    # 3. Flip back to the original state
    for i in range(qubits.size()):
        cudaq.x(qubits[i])


# --- 2. The Diffusion Operator (Amplifies the search amplitude) ---
@cudaq.kernel
def grover_diffusion(qubits: cudaq.qvector):
    # This implements the diffusion operation D = -H^n * O_0 * H^n
    n = qubits.size()

    # 1. Apply Hadamard gates
    for i in range(n):
        cudaq.h(qubits[i])

    # 2. Apply the phase flip to the state |00...0> (the O_0 part)
    # The oracle for |00...0> is equivalent to:
    #   Hadamard -> Phase flip all (X-gates) -> MCZ -> Phase flip all (X-gates) -> Hadamard

    # Flip all to |11...1>
    for i in range(n):
        cudaq.x(qubits[i])

    # Apply the multi-controlled Z on the |11...1> state
    cudaq.z.ctrl(qubits)

    # Flip back to |00...0>
    for i in range(n):
        cudaq.x(qubits[i])

    # 3. Apply Hadamard gates again
    for i in range(n):
        cudaq.h(qubits[i])


# --- 3. Full Grover's Search Circuit ---
@cudaq.kernel
def grover_search(n_qubits: int, iterations: int):
    qubits = cudaq.qalloc(n_qubits)

    # Step 1: Create uniform superposition (Hadamard layer)
    for i in range(n_qubits):
        cudaq.h(qubits[i])

    # Step 2: Apply the Grover iteration (Oracle + Diffusion)
    for _ in range(iterations):
        grover_oracle(qubits)
        grover_diffusion(qubits)

    # Step 3: Measure the result
    cudaq.mz(qubits)

# --- Execution ---
# Configure the simulator to use the GPU (the 'nvidia' target is usually used for full state-vector)
# Note: You need a correctly configured CUDA-Q environment for GPU acceleration.
# cudaq.set_target('nvidia')

# Run the simulation
counts = cudaq.sample(grover_search, NUM_QUBITS, NUM_ITERATIONS, shots=1000)

# --- Analysis ---
# The solution is expected to be the state with the highest count: '1' * 24
solution_state = '1' * NUM_QUBITS

print(f"Search Results (Top 5):")
# Convert counts to a dictionary and sort by value (count)
sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

i = 0
for state, count in sorted_counts.items():
    if i >= 5:
        break

    probability = count / sum(counts.values()) * 100
    if state == solution_state:
        print(f"-> SOLUTION STATE: {state} | Count: {count} ({probability:.2f}%)")
    else:
        print(f"   Other State:    {state} | Count: {count} ({probability:.2f}%)")
    i += 1