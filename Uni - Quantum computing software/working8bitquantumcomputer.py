import cudaq
import sys
# The gate names are injected by the decorator, no need to import them.

# Setting a high recursion limit for good measure
sys.setrecursionlimit(5000)

NUM_BITS = 8
TOTAL_QUBITS = 2 * NUM_BITS

# ----------------------------------------------------
# 1. Quantum Kernel Definition (FINAL WORKING STRUCTURE)
# ----------------------------------------------------
@cudaq.kernel
def xor_adder_kernel(x_init_data: list[int]):
    """
    Implements the 8-bit XOR sum. The qvector is created INSIDE the kernel
    to satisfy the argument packing requirement.

    x_init_data list format: [A_MSB, ..., A_LSB, B_MSB, ..., B_LSB]
    """
    # FIX: The qvector must be instantiated here, inside the decorated function.
    q = cudaq.qvector(TOTAL_QUBITS)

    # --- State Preparation (Initialize inputs using the passed list) ---

    # Initialize A register (q[0] to q[7] -> LSB to MSB)
    for i in range(NUM_BITS):
        # List index for A bit i (from LSB) is (NUM_BITS - 1 - i)
        if x_init_data[NUM_BITS - 1 - i] == 1:
            x(q[i])

    # Initialize B register (q[8] to q[15] -> LSB to MSB)
    for i in range(NUM_BITS):
        # List index for B bit i (from LSB) is (TOTAL_QUBITS - 1 - i)
        if x_init_data[TOTAL_QUBITS - 1 - i] == 1:
            x(q[i + NUM_BITS])


    # --- XOR Sum Logic (A XOR B) - Manually Unrolled CNOTs ---
    # Control A_i (q[i]), Target B_i (q[i + 8])
    cx(q[0], q[8])   # LSB
    cx(q[1], q[9])
    cx(q[2], q[10])
    cx(q[3], q[11])
    cx(q[4], q[12])
    cx(q[5], q[13])
    cx(q[6], q[14])
    cx(q[7], q[15])  # MSB

    # --- Measurement ---
    # Measure the B register (which holds the XOR sum)
    mz(q[8:])


# ----------------------------------------------------
# 2. Interactive Driver Logic
# ----------------------------------------------------

def run_quantum_xor_prompt():

    print(f"\n--- {NUM_BITS}-Bit Quantum XOR Sum (A XOR B) ---")
    print(f"Enter two decimal numbers (0 to {2**NUM_BITS - 1}).")

    try:
        A = int(input("Enter first number (A): "))
        B = int(input("Enter second number (B): "))

        if not (0 <= A < 256 and 0 <= B < 256):
            print("\nWarning: Inputs outside the 8-bit range (0-255).")

        # Classical Logic: Convert Decimals to Binary Lists (8 elements: [MSB, ..., LSB])
        A_bits = [int(bit) for bit in format(A, f'0{NUM_BITS}b')]
        B_bits = [int(bit) for bit in format(B, f'0{NUM_BITS}b')]

        # --- Prepare the flat list of initialization data ---
        # Format: [A_MSB, ..., A_LSB, B_MSB, ..., B_LSB] (16 elements total)
        x_init_data = A_bits + B_bits

        # --- Sample the kernel ---
        # FIX: Remove the qvector argument from the sample call.
        result = cudaq.sample(xor_adder_kernel, x_init_data)

        # Quantum Result Processing
        most_probable_state = result.most_probable()

        # The result is the measured B register, LSB first. Reverse it for MSB first.
        measured_sum_reversed = most_probable_state
        xor_binary_string = measured_sum_reversed[::-1]
        quantum_sum_decimal = int(xor_binary_string, 2)

        # Classical verification
        expected_sum_decimal = A ^ B

        print("-" * 40)
        print(f"Classical Expectation (A XOR B): {A} ^ {B} = {expected_sum_decimal}")
        print(f"Binary Check: {format(A, f'0{NUM_BITS}b')} XOR {format(B, f'0{NUM_BITS}b')}")
        print("-" * 40)

        print(f"Quantum Measurement (XOR Sum): {xor_binary_string}")
        print(f"Quantum Sum (Decimal): {quantum_sum_decimal}")

        if quantum_sum_decimal == expected_sum_decimal:
            print("STATUS: SUCCESS ✅ - Quantum result matches classical XOR sum.")
        else:
            print("STATUS: FAILURE ❌ - Check quantum circuit logic.")

    except ValueError as e:
        print(f"\nError: {e}")
        print("Please restart the script and enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    run_quantum_xor_prompt()