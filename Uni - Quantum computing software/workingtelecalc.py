import cudaq

# ----------------------------------------------------
# 1. Quantum Kernel Definition (Teleportation)
# ----------------------------------------------------
@cudaq.kernel
def teleportation_kernel():
    """
    Teleports the state of Qubit A to Qubit C using Qubit B as the entangled link.
    Requires H, CNOT, and measurements.
    """
    # Allocate 3 qubits:
    # Qubit A: State to be teleported (Source)
    # Qubit B: Entangled partner (Link)
    # Qubit C: Final state (Destination)
    q = cudaq.qvector(3)
    qA, qB, qC = q[0], q[1], q[2]

    # --- Part 1: State Preparation ---
    # 1. Prepare the state to be teleported on Qubit A (Let's use |1> for easy testing)
    x(qA) # Applies the X gate, setting the state of A to |1>

    # 2. Create the Bell pair (entangled link) between Qubit B and Qubit C
    h(qB)  # Hadamard on Qubit B
    cx(qB, qC) # CNOT: Control B, Target C (Creates the Bell state |Φ+>)

    # --- Part 2: Bell State Measurement (Alice's side) ---
    # 3. Apply the CNOT from the source (A) to the link (B)
    cx(qA, qB) # CNOT: Control A, Target B

    # 4. Apply the Hadamard to the source (A)
    h(qA)

    # 5. Measure Qubit A and Qubit B
    mz(qA)
    mz(qB)

    # --- Part 3: Classical Correction (Bob's side) ---
    # We will let the simulator perform the classical correction based on the measurements of qA and qB.
    # The X gate is applied if qB measures 1. The Z gate is applied if qA measures 1.

    # Read classical measurement results from Qubit A and Qubit B
    # Since the sample() function simulates this, we can rely on a simplified approach
    # within the kernel using conditional gates.

    # If the measurement of qB is 1, apply X to qC.
    if mz(qB):
        x(qC)

    # If the measurement of qA is 1, apply Z to qC.
    if mz(qA):
        z(qC)

    # --- Part 4: Final Measurement ---
    # 6. Measure Qubit C to verify the teleported state
    mz(qC)

# ----------------------------------------------------
# 2. Test Driver Code
# ----------------------------------------------------

def run_teleportation_test():

    # The state prepared on Qubit A was |1>.
    expected_state = 1

    try:
        kernel = teleportation_kernel

        # Execute the kernel
        result = cudaq.sample(kernel)

        # The result keys are the bit strings for qA, qB, qC (in order of measurement).
        # We only care about the last measured qubit, qC.
        measured_state = result.most_probable()

        # Get the measurement result of Qubit C (the very last measurement)
        measured_c = int(measured_state[-1])

        print(f"\n--- TEST: Quantum Teleportation (State |{expected_state}⟩ from A to C) ---")

        if measured_c == expected_state:
            print(f"Final State on Qubit C (Destination): |{measured_c}⟩")
            print("STATUS: SUCCESS ✅ - State Teleported.")
        else:
            print(f"Final State on Qubit C (Destination): |{measured_c}⟩")
            print(f"Error: Expected |{expected_state}⟩")
            print("STATUS: FAILURE ❌")

    except Exception as e:
        print(f"--- TEST FAILED ---")
        print(f"Runtime Error during kernel execution or compilation: {e}")


# ----------------------------------------------------
# 3. Execution
# ----------------------------------------------------

run_teleportation_test()