from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
import hashlib
import time
import numpy as np

# --- Configuration ---
NUM_BITS_PER_RUN = 8
NUM_RUNS = 32         # 256 bits total for the hash seed
SHOTS = 1

# --- 1. Define the Quantum Circuit (WITH MEASUREMENT) ---
def create_lattice_qrng_circuit(num_qubits):
    """Creates the 8-qubit circuit WITH the final Measurement."""
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

    # CRITICAL FIX: Re-add the measurement operation
    circuit.measure(range(num_qubits), range(num_qubits))

    return circuit

# --- 2. Main Execution and Hashrate Calculation ---
if __name__ == "__main__":

    qrng_circuit = create_lattice_qrng_circuit(NUM_BITS_PER_RUN)
    simulator = BasicSimulator()

    total_hashes = 0
    start_time = time.time()

    print("--- Starting Quantum-Seeded Hashrate Test (INFINITE LOOP) ---")
    print("Monitor your CPU usage now. Press Ctrl+C to stop and see final stats.")

    # --- The Infinite Hashrate Loop ---
    try:
        while True:

            current_hash_start_time = time.time()
            raw_quantum_bits = ""

            # 1. BATCHED QUANTUM RANDOMNESS GENERATION (32 runs)
            for _ in range(NUM_RUNS):
                compiled_circuit = transpile(qrng_circuit, simulator)
                job = simulator.run(compiled_circuit, shots=SHOTS)

                # The simulator returns counts from the result
                counts = job.result().get_counts()

                # Extract the random 8-bit string
                random_binary_little_endian = list(counts.keys())[0]
                raw_quantum_bits += random_binary_little_endian[::-1] # Convert to big-endian

            # 2. QUANTUM-RESISTANT HASHING (SHAKE256)
            seed_data = raw_quantum_bits.encode('utf-8')
            hash_object = hashlib.shake_256()
            hash_object.update(seed_data)
            final_hash = hash_object.hexdigest(32)

            total_hashes += 1

            # --- Real-Time Hashrate Calculation ---
            current_hash_end_time = time.time()
            time_for_this_hash = current_hash_end_time - current_hash_start_time

            # Instantaneous H/s: 1 hash / time_for_this_hash
            instant_hashrate = 1.0 / time_for_this_hash

            print(f"Hash #{total_hashes}: {final_hash[:16]}... | Rate: {instant_hashrate:.2f} H/s")

    except KeyboardInterrupt:
        # User pressed Ctrl+C
        pass

    # --- Final Results ---
    end_time = time.time()
    total_time = end_time - start_time

    # Calculate Average Hashes Per Second (H/s)
    average_hashrate = total_hashes / total_time

    print("\n" + "=" * 60)
    print("--- Final Average Hashrate Results ---")
    print(f"Total Hashes Generated: {total_hashes}")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Average Hashrate Over Test: **{average_hashrate:.2f} H/s**")
    print("=" * 60)
