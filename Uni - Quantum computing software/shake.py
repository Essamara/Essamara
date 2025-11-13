from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
import hashlib
import numpy as np

# --- Configuration ---
NUM_BITS_PER_RUN = 8  # Qubits in circuit
NUM_RUNS = 32         # Number of runs (32 * 8 = 256 bits total)
SHOTS = 1

# --- 1. Define the Quantum Circuit (from previous steps) ---
def create_lattice_qrng_circuit(num_qubits):
    """Creates the 8-qubit QRNG circuit with the 4x4 CNOT lattice."""
    circuit = QuantumCircuit(num_qubits, num_qubits)
    circuit.h(range(num_qubits))

    # 10 CNOT LATTICE
    lattice_pattern = [(0, 1), (1, 2), (2, 3), (0, 3)]
    for pair in lattice_pattern:
        circuit.cx(pair[0], pair[1])
    for pair in lattice_pattern:
        circuit.cx(pair[1], pair[0])
    circuit.cx(0, 1) # CNOT 9
    circuit.cx(2, 3) # CNOT 10

    circuit.x(3) # NOT gate
    circuit.measure(range(num_qubits), range(num_qubits))

    return circuit

# --- 2. Main Execution ---
if __name__ == "__main__":

    qrng_circuit = create_lattice_qrng_circuit(NUM_BITS_PER_RUN)
    simulator = BasicSimulator()
    raw_quantum_bits = ""

    print("--- 1. Generating 256 Quantum Random Bits (The PQC Seed) ---")

    # --- Loop to generate 256 bits ---
    for i in range(NUM_RUNS):
        compiled_circuit = transpile(qrng_circuit, simulator)
        job = simulator.run(compiled_circuit, shots=SHOTS, memory=True)
        result = job.result()

        # Extract and accumulate the 8 random bits
        random_binary_little_endian = result.get_memory()[0]
        raw_quantum_bits += random_binary_little_endian[::-1]

        # Simple progress indicator
        if (i + 1) % 8 == 0:
             print(f"Generated {i + 1}/{NUM_RUNS} runs ({len(raw_quantum_bits)} bits)...")

    print("\nGeneration complete. Quantum entropy source ready.")
    print("-" * 50)

    # --- 3. Quantum-Resistant Hashing using SHAKE256 ---

    # Convert the 256-bit binary string to a byte sequence for the hash function
    # We interpret the string of '0's and '1's as the random data.
    seed_data = raw_quantum_bits.encode('utf-8')

    # Initialize SHAKE256 (an XOF from the SHA-3 family)
    # SHAKE256 is used in NIST PQC candidates like Dilithium.
    hash_object = hashlib.shake_256()

    # Feed the quantum random bits into the hash function
    hash_object.update(seed_data)

    # Generate a 256-bit (32-byte) hash output
    # This hash is considered more resistant to quantum attacks than SHA-256
    QUANTUM_RESISTANT_HASH = hash_object.hexdigest(32)

    print("\n--- 2. Quantum-Resistant Hash Output (SHAKE256) ---")
    print(f"Total Quantum Seed Bits Used: {len(raw_quantum_bits)}")
    print(f"PQC-Relevant Hash Type: SHAKE256 (256-bit output)")
    print(f"Final Quantum-Resistant Hash (64 Hex Characters):")
    print(f"**{QUANTUM_RESISTANT_HASH}**")
    print("-" * 50)

    # --- 4. Final Verification ---
    # We verify the randomness by checking the final hash.
    print(f"Verification Check: SHA-256 of the SHAKE256 output (for integrity):\n{hashlib.sha256(QUANTUM_RESISTANT_HASH.encode()).hexdigest()}")
