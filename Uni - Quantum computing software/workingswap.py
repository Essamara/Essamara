import cudaq

# ----------------------------------------------------
# 1. Quantum Kernel Definition (SWAP Gate)
# ----------------------------------------------------
@cudaq.kernel
def swap_kernel(a_val: int, b_val: int):
    """
    Implements the SWAP gate using three CNOT (cx) gates.
    This avoids the problematic recursive decomposition of CCX/Toffoli.
    """

    # Allocate qubits
    a_qubit = cudaq.qubit()
    b_qubit = cudaq.qubit()

    # 1. Initialize qubits based on classical inputs
    if a_val == 1:
        x(a_qubit)
    if b_val == 1:
        x(b_qubit)

    # 2. Apply the SWAP gate decomposition (three CNOTs)
    # CNOT 1: Control A, Target B
    cx(a_qubit, b_qubit)

    # CNOT 2: Control B, Target A
    cx(b_qubit, a_qubit)

    # CNOT 3: Control A, Target B
    cx(a_qubit, b_qubit)

    # 3. Measure the results
    mz(a_qubit)
    mz(b_qubit)


# ----------------------------------------------------
# 2. Test Driver Code
# ----------------------------------------------------

def run_swap_test(a, b):
    """Executes the kernel and prints the result for a single test case."""

    # Expected result: state of A and B are swapped.
    expected_a = b
    expected_b = a

    try:
        kernel = swap_kernel

        # Execute the kernel
        result = cudaq.sample(kernel, a, b)

        # The result keys are the bit strings for a_qubit and b_qubit, typically in the order they were measured.
        measured_state = result.most_probable()

        # Assuming the order is [a_qubit, b_qubit] as per typical measurement conventions
        measured_a = int(measured_state[0])
        measured_b = int(measured_state[1])

        print(f"\n--- TEST: Swap ({a}, {b}) ---")
        print(f"Initial State |{a}{b}⟩")

        if measured_a == expected_a and measured_b == expected_b:
            print(f"Final State: |{measured_a}{measured_b}⟩")
            print("STATUS: SUCCESS ✅ - State Swapped.")
        else:
            print(f"Final State: |{measured_a}{measured_b}⟩")
            print(f"Error: Expected |{expected_a}{expected_b}⟩")
            print("STATUS: FAILURE ❌")

    except Exception as e:
        print(f"--- TEST: Swap ({a}, {b}) FAILED ---")
        print(f"Runtime Error during kernel execution or compilation: {e}")


# ----------------------------------------------------
# 3. Execution
# ----------------------------------------------------

# Test 1: Swap (1, 0) -> Expected (0, 1)
run_swap_test(1, 0)

# Test 2: Swap (0, 1) -> Expected (1, 0)
run_swap_test(0, 1)

# Test 3: Swap (1, 1) -> Expected (1, 1)
run_swap_test(1, 1)