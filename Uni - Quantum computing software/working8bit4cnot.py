import cudaq
import sys

sys.setrecursionlimit(5000)

NUM_CONTROLS = 4
TOTAL_QUBITS_FOR_TEST = NUM_CONTROLS + 1 # 5 qubits
TOTAL_QUBITS_OVERALL = 16

# ----------------------------------------------------
# 1. Quantum Kernel Definition: Quadruple CNOT Test
# ----------------------------------------------------
@cudaq.kernel
def quadruple_cnot_kernel():
    """
    Tests a 4-Control CNOT (CCN-CNOT) gate on 5 qubits.
    q[0]-q[3] are Controls, q[4] is the Target.
    """
    q = cudaq.qvector(TOTAL_QUBITS_OVERALL)

    # 1. State Preparation: Set ALL 4 Control qubits to |1>
    x(q[0])
    x(q[1])
    x(q[2])
    x(q[3])

    # Target qubit
    target = q[4]

    # 2. Quadruple CNOT Operation: Apply X gate controlled by 4 qubits
    # FIX: Manually specify all controls as individual arguments.
    x.ctrl(q[0], q[1], q[2], q[3], target)

    # 3. Measurement: Only measure the 5 qubits involved in the test
    mz(q[0:TOTAL_QUBITS_FOR_TEST])

# ----------------------------------------------------
# 2. Driver Logic
# ----------------------------------------------------

def run_quadruple_cnot_test():

    print("\n--- 5-Qubit Quadruple CNOT (4-Control X) Test ---")
    print("Using manually specified individual arguments for controls.")
    print(f"Controls: q[0], q[1], q[2], q[3] | Target: q[4]")
    print("-" * 65)

    result = cudaq.sample(quadruple_cnot_kernel)
    most_probable_state = result.most_probable()
    expected_state = "1" * TOTAL_QUBITS_FOR_TEST # "11111"

    print(f"Most Probable Measured State: {most_probable_state}")

    if most_probable_state == expected_state:
        print(f"STATUS: SUCCESS ✅ - Quadruple CNOT implemented successfully, resulting in **{expected_state}**.")
    else:
        print("STATUS: FAILURE ❌ - Compiler is incompatible with this multi-control syntax.")

if __name__ == "__main__":
    run_quadruple_cnot_test()