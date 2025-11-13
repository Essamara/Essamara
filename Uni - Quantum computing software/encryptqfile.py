import os
from qiskit import QuantumCircuit, transpile
from qiskit.providers.basic_provider import BasicSimulator
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- Configuration ---
NUM_BITS_PER_RUN = 8
NUM_RUNS = 32
SHOTS = 1

INPUT_FILENAME = "image.png"
ENCRYPTED_FILENAME = "image.png.enc"
DECRYPTED_FILENAME = "image_decrypted.png"

# --- 1. Define the Quantum Circuit (Your QRNG) ---
def create_lattice_qrng_circuit(num_qubits):
    """Creates the 8-qubit QRNG circuit with the 4x4 CNOT lattice."""
    circuit = QuantumCircuit(num_qubits, num_qubits)
    circuit.h(range(num_qubits))

    # 10 CNOT LATTICE (as in your original code)
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

# --- 2. Key Derivation from QRNG (Your SHAKE256 Logic) ---
def generate_quantum_key():
    """Generates a 32-byte (256-bit) key using QRNG and SHAKE256."""
    qrng_circuit = create_lattice_qrng_circuit(NUM_BITS_PER_RUN)
    simulator = BasicSimulator()
    raw_quantum_bits = ""

    print("--- 1. Generating 256 Quantum Random Bits (The Key Seed) ---")
    for _ in range(NUM_RUNS):
        compiled_circuit = transpile(qrng_circuit, simulator)
        job = simulator.run(compiled_circuit, shots=SHOTS, memory=True)
        result = job.result()
        random_binary_little_endian = result.get_memory()[0]
        raw_quantum_bits += random_binary_little_endian[::-1]

    print(f"Total Quantum Seed Bits Used: {len(raw_quantum_bits)}")

    # Convert the 256-bit binary string to a byte sequence
    seed_data = raw_quantum_bits.encode('utf-8')

    # Use SHAKE256 to create a 32-byte (256-bit) key
    hash_object = hashlib.shake_256()
    hash_object.update(seed_data)

    # Return the raw 32 bytes needed for AES-256
    return hash_object.digest(32)

# --- 3. Encryption and Decryption Functions (AES-256 GCM) ---
def encrypt_file(key, input_path, output_path):
    """Encrypts a file using AES-256 in GCM mode."""
    # AES-256 requires a 96-bit (12-byte) unique Nonce (IV/initialization vector)
    nonce = os.urandom(12)

    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    with open(input_path, 'rb') as f_in:
        plaintext = f_in.read()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Write the Nonce (required for decryption), the Ciphertext, and the Tag
    with open(output_path, 'wb') as f_out:
        f_out.write(nonce)
        f_out.write(encryptor.tag)
        f_out.write(ciphertext)

    print(f"Encryption successful. Data saved to: {output_path}")
    print(f"Key (First 8 bytes): {key.hex()[:16]}...")
    return nonce # Return the nonce for the demo

def decrypt_file(key, input_path, output_path, nonce):
    """Decrypts a file using AES-256 in GCM mode."""
    # We must read the Nonce (12 bytes) and the Tag (16 bytes) first
    with open(input_path, 'rb') as f_in:
        nonce_file = f_in.read(12)
        tag = f_in.read(16)
        ciphertext = f_in.read()

    # The GCM mode needs the original Nonce and Tag for verification
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce_file, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        with open(output_path, 'wb') as f_out:
            f_out.write(plaintext)

        print(f"Decryption successful. Data saved to: {output_path}")
    except Exception as e:
        print(f"Decryption FAILED! Authentication Tag verification failed (Key/Data corrupted). Error: {e}")

# --- 4. Main Execution ---
if __name__ == "__main__":

    # 1. Create a dummy file for the demonstration if it doesn't exist
    if not os.path.exists(INPUT_FILENAME):
        print(f"\nNOTE: Creating a dummy file named '{INPUT_FILENAME}' for the demo...")
        with open(INPUT_FILENAME, 'w') as f:
            f.write("This is the secret data for the PNG file (pretend this is image data).")

    print("\n" + "=" * 60)
    print("STARTING QUANTUM-ENHANCED ENCRYPTION PROCESS")
    print("=" * 60)

    # 2. GENERATE KEY from QRNG/SHAKE256
    quantum_key_256bit = generate_quantum_key()
    print("-" * 60)

    # 3. ENCRYPT FILE
    print(f"--- 2. Encrypting '{INPUT_FILENAME}' ---")
    encrypt_file(quantum_key_256bit, INPUT_FILENAME, ENCRYPTED_FILENAME)
    print("-" * 60)

    # 4. DECRYPT FILE
    print(f"--- 3. Decrypting '{ENCRYPTED_FILENAME}' ---")
    # Note: We don't use the nonce returned from encrypt_file here;
    # the function reads it from the beginning of the encrypted file.
    decrypt_file(quantum_key_256bit, ENCRYPTED_FILENAME, DECRYPTED_FILENAME, None)
    print("=" * 60)