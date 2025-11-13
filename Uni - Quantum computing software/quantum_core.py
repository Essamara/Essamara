import sys
import numpy as np
import cudaq

# Set the recursion limit for stability
sys.setrecursionlimit(5000)
# Set the quantum target
cudaq.set_target("nvidia")

# ====================================================================
# NOTE: ASSUMES bell_state.py AND quantum_search.py ARE PRESENT.
# These imports are REQUIRED for 'transfer' and 'search' commands.
# ====================================================================
try:
    # IMPORTANT: Replace the dummy content in bell_state.py and quantum_search.py
    # with your actual CUDA-Q implementation.
    from bell_state import teleport_quantum_state
    from quantum_search import grover_search
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import helper module. Make sure bell_state.py and quantum_search.py are present. Error: {e}")
    # The script will continue, but 'transfer' and 'search' will fail if the modules are missing/empty.


# --- CORE TRANSLATION/API FUNCTIONS ---

def classical_command_to_quantum(command_line: str):
    """
    Simulates the 'Wine' layer: translates a simple classical command
    into a structured quantum routine, running it on the quantum core.
    """
    parts = command_line.strip().lower().split()
    if not parts:
        return "[Wine Layer] Error: Command cannot be empty."

    command = parts[0]
    args = parts[1:]

    print(f"\n[Wine Layer] Translating classical command '{command_line}' to quantum operations...")

    try:
        # ----------------------------------
        # --- 1. TELEPORTATION (transfer) ---
        # ----------------------------------
        if command == 'transfer':
            message_angle = np.pi / 4
            teleported_z_exp = teleport_quantum_state(message_angle)
            initial_z_exp = np.cos(message_angle)

            if abs(initial_z_exp - teleported_z_exp) < 0.01:
                return f"[Quantum Core: Teleportation Success] Data secure. Initial <Z>:{initial_z_exp:.4f}, Teleported <Z>:{teleported_z_exp:.4f}. Error: {abs(initial_z_exp - teleported_z_exp):.4f}."
            else:
                return f"[Quantum Core: Teleportation Failure] Transfer degraded. Error too large."

        # ----------------------------------
        # --- 2. SEARCH (search) -----------
        # ----------------------------------
        elif command == 'search':
            target = '11'
            result = grover_search(n_qubits=2, iterations=1, target_state=target, shots_count=10000)

            if result['most_likely'] == target and result['success_rate'] > 99.0:
                 return f"[Quantum Core: Search Success] Target '{target}' found with {result['success_rate']:.2f}% certainty. Search was exponentially faster than classical."
            else:
                 return f"[Quantum Core: Search Failure] Low confidence. Found {result['most_likely']} with {result['success_rate']:.2f}%."

        # ----------------------------------
        # --- 3. BASIC OPS (qubit_op) ------
        # ----------------------------------
        elif command == 'qubit_op':
            if len(args) != 3:
                return f"[Wine Layer] Error: 'qubit_op' requires GATE, INITIAL STATE, and MEASUREMENT BASIS. Format: qubit_op [X|S|H] [0|1] [X|Y|Z]. Example: qubit_op H 0 X"

            gate_str = args[0].upper()
            initial_state_str = args[1]
            basis_str = args[2].upper()

            if gate_str not in ['X', 'S', 'H'] or initial_state_str not in ['0', '1'] or basis_str not in ['X', 'Y', 'Z']:
                return f"[Wine Layer] Error: Invalid arguments. Supported Gates: X, S, H. Supported Initial States: 0, 1. Supported Bases: X, Y, Z."

            shots = 10000
            kernel = cudaq.make_kernel()
            q = kernel.qalloc(1)

            # 1. Set the initial state
            if initial_state_str == '1':
                kernel.x(q[0])

            # 2. Apply the requested gate
            gate_map = {
                'X': kernel.x,
                'S': kernel.s,
                'H': kernel.h
            }
            gate_map[gate_str](q[0])

            # 3. Apply Change-of-Basis Gates
            if basis_str == 'X':
                # Rotate X onto Z: Apply H
                kernel.h(q[0])
            elif basis_str == 'Y':
                # Rotate Y onto Z: Apply S† then H
                kernel.sdg(q[0])
                kernel.h(q[0])

            # 4. Measure
            kernel.mz(q)

            # Execute and get results
            result = cudaq.sample(kernel, shots_count=shots)

            # Format results for output
            output = f"[Quantum Core: Single Qubit Operation ({gate_str})]\n"
            output += f"Initial State: |{initial_state_str}>\n"
            output += f"Gate Applied: {gate_str}-gate\n"
            output += f"Measurement Basis: **{basis_str}**\n"
            output += f"Measurement Result (Shots={shots}):\n"

            # Calculate probabilities and format counts
            result_display = []
            for state, count in result.items():
                prob = count / shots * 100
                if basis_str == 'X':
                    state_label = f"|{state}>_X"
                elif basis_str == 'Y':
                    state_label = f"|{state}>_Y"
                else:
                    state_label = f"|{state}>"

                result_display.append(f"State {state_label}: {count} counts ({prob:.2f}%)")

            output += "\n".join(result_display)

            return output

        else:
            return f"[Wine Layer] Error: Unknown classical command '{command}'. Available: 'transfer', 'search', 'qubit_op [X|S|H] [0|1] [X|Y|Z]'."

    except Exception as e:
        return f"[Quantum Core: Routine Error] Execution failed for command '{command}': {e}"

if __name__ == "__main__":
    print("--- QUANTUM CORE API TEST ---")
    # Test a command that relies only on CUDA-Q and numpy
    print(f"Result (H 0 X): {classical_command_to_quantum('qubit_op H 0 X')}")
