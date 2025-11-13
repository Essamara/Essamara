import cudaq
import numpy as np

# Set the target for simulation
cudaq.set_target("nvidia")

def teleport_quantum_state(message_angle: float) -> float:
    """
    Implements the Quantum Teleportation protocol using CUDA-Q and returns
    the Z expectation value (<Z>) of the teleported qubit (Bob's Qubit 2).

    Args:
        message_angle: The RY angle (in radians) to prepare the initial state.

    Returns:
        The measured Z expectation value on the receiver qubit (Qubit 2).
    """
    kernel = cudaq.make_kernel()

    # Allocate 3 qubits: Q0 (Message), Q1 (Alice), Q2 (Bob/Receiver).
    qubits = kernel.qalloc(3)

    # --- PART 1: PREPARATION ---
    # 1. Prepare the entangled channel (Bell pair) between Alice (Q1) and Bob (Q2).
    kernel.h(qubits[1])
    kernel.cx(qubits[1], qubits[2])

    # 2. Prepare the Message (Qubit 0) in a known state (RY gate).
    kernel.ry(message_angle, qubits[0])

    # --- PART 2: TELEPORTATION LOGIC ---
    # 3. Alice applies the Bell state measurement circuit (CX + H) to her two qubits (Q0 and Q1).
    kernel.cx(qubits[0], qubits[1])
    kernel.h(qubits[0])

    # 4. Classical corrections (implemented using controlled gates on Bob's qubit Q2).
    # Controlled-X correction based on Q1 measurement.
    kernel.cx(qubits[1], qubits[2])
    # Controlled-Z correction based on Q0 measurement.
    kernel.cz(qubits[0], qubits[2])

    # --- PART 3: VERIFICATION (Measurement) ---
    # Measure all qubits to get the sample counts (we only care about Qubit 2).
    kernel.mz(qubits)

    # Execute the kernel 10,000 times (shots)
    shots = 10000
    sample_result = cudaq.sample(kernel, shots_count=shots)

    # Calculate the Z expectation value from the measurement counts on Qubit 2 (Bob).
    z_exp_sum = 0
    for bits, count in sample_result.items():
        # Qubit 2 result is the rightmost bit (index 2 in the string)
        if bits[2] == '0':
            z_exp_sum += count
        else: # bit is '1'
            z_exp_sum -= count

    teleported_z_exp = z_exp_sum / shots

    # NOTE: The initial Z expectation is calculated in quantum_core.py for comparison.
    return teleported_z_exp

# Example execution block (optional, used for direct testing)
if __name__ == '__main__':
    angle = np.pi / 4
    initial_z = np.cos(angle)
    teleported_z = teleport_quantum_state(angle)

    print("--- Quantum Teleportation Test ---")
    print(f"Initial <Z>: {initial_z:.8f}")
    print(f"Teleported <Z>: {teleported_z:.8f}")
    print(f"Error: {abs(initial_z - teleported_z):.8f}")
