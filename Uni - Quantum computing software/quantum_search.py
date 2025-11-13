import cudaq
import numpy as np
import sys

# Set the target for simulation
cudaq.set_target("nvidia")

def apply_oracle(kernel: cudaq.Kernel, qubits, target_state: str):
    """Applies the Grover's oracle for a 2-qubit system."""

    if target_state == '00':
        kernel.x(qubits[0])
        kernel.x(qubits[1])
        kernel.cz(qubits[0], qubits[1])
        kernel.x(qubits[0])
        kernel.x(qubits[1])
    elif target_state == '01':
        kernel.x(qubits[0])
        kernel.cz(qubits[0], qubits[1])
        kernel.x(qubits[0])
    elif target_state == '10':
        kernel.x(qubits[1])
        kernel.cz(qubits[0], qubits[1])
        kernel.x(qubits[1])
    elif target_state == '11':
        # Target state '11' requires only the controlled-Z gate
        kernel.cz(qubits[0], qubits[1])
    else:
        raise ValueError("Target state must be '00', '01', '10', or '11' for 2 qubits.")

def apply_diffuser(kernel: cudaq.Kernel, qubits):
    """Applies the 2-qubit Grover's diffusion operator (Amplification)."""

    # 1. Apply Hadamard gates
    kernel.h(qubits)

    # 2. Apply the oracle for state |00> (Reflection about the |00> state)
    kernel.x(qubits)
    kernel.cz(qubits[0], qubits[1])
    kernel.x(qubits)

    # 3. Apply Hadamard gates again
    kernel.h(qubits)

def grover_search(n_qubits: int, iterations: int, target_state: str, shots_count: int) -> dict:
    """
    Implements Grover's search algorithm for n=2 qubits using CUDA-Q.
    """
    if n_qubits != 2:
        raise NotImplementedError("This implementation is currently limited to n_qubits=2.")

    if len(target_state) != n_qubits:
         raise ValueError(f"Target state length must match n_qubits ({n_qubits}).")

    # Set the recursion limit for stability (for some environments)
    sys.setrecursionlimit(5000)

    kernel = cudaq.make_kernel()
    qubits = kernel.qalloc(n_qubits)

    # 1. Prepare in uniform superposition state |s>
    kernel.h(qubits)

    # 2. Apply the Grover iteration (Oracle + Diffuser)
    for _ in range(iterations):
        apply_oracle(kernel, qubits, target_state)
        apply_diffuser(kernel, qubits)

    # 3. Measure
    kernel.mz(qubits)

    # Execute the kernel
    sample_result = cudaq.sample(kernel, shots_count=shots_count)

    # 4. Process results
    total_shots = shots_count
    max_counts = 0
    most_likely_state = '00'
    target_counts = 0

    for state, count in sample_result.items():
        if count > max_counts:
            max_counts = count
            most_likely_state = state

        if state == target_state:
            target_counts = count

    success_rate = (target_counts / total_shots) * 100

    return {
        'results': sample_result,
        'most_likely': most_likely_state,
        'success_rate': success_rate
    }
