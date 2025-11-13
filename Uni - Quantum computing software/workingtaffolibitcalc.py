import cudaq

# ----------------------------------------------------
# 1. Quantum Kernel Definition (Full Adder Sum Bit)
# ----------------------------------------------------
@cudaq.kernel
def full_adder_kernel(a_val: int, b_val: int, cin_val: int):
    """
    Creates a quantum kernel for the full adder's SUM bit (A XOR B XOR C_in).
    """
    # Allocate qubits
    a_qubit = cudaq.qubit()
    b_qubit = cudaq.qubit()
    cin_qubit = cudaq.qubit()

    # Initialize qubits based on classical inputs
    if a_val == 1:
        x(a_qubit) # CORRECTED: Removed 'cudaq.'
    if b_val == 1:
        x(b_qubit) # CORRECTED: Removed 'cudaq.'
    if cin_val == 1:
        x(cin_qubit) # CORRECTED: Removed 'cudaq.'

    # Apply the quantum circuit for Sum
    # cx is CNOT (XOR operation)

    # a_qubit = a_qubit XOR b_qubit
    cx(b_qubit, a_qubit) # CORRECTED: Removed 'cudaq.'

    # a_qubit = a_qubit XOR cin_qubit (Final Sum)
    cx(cin_qubit, a_qubit) # CORRECTED: Removed 'cudaq.'

    # Measure the result
    mz(a_qubit) # CORRECTED: Removed 'cudaq.'


# ----------------------------------------------------
# 2. Test Driver Code (Non-Recursive, No Shots)
# ----------------------------------------------------

def run_full_adder_test(a, b, cin):
    """Executes the kernel and prints the result for a single test case."""

    expected_sum = a ^ b ^ cin

    try:
        kernel = full_adder_kernel

        # Execute the kernel without shots_count
        result = cudaq.sample(kernel, a, b, cin)

        measured_state = result.most_probable()
        measured_sum = int(measured_state)

        print(f"--- TEST: {a} + {b} + {cin} (Full Adder Sum) ---")

        if measured_sum == expected_sum:
            print(f"Result: {measured_sum}")
            print("SUCCESS")
        else:
            print(f"Error: Measured Sum {measured_sum} != Expected Sum {expected_sum}")
            print("FAILURE")

    except Exception as e:
        print(f"--- TEST: {a} + {b} + {cin} FAILED ---")
        print(f"Runtime Error during kernel execution or compilation: {e}")


# ----------------------------------------------------
# 3. Execution
# ----------------------------------------------------

# Test 1: 1 + 0 + 0. Expected Sum is 1.
run_full_adder_test(1, 0, 0)