import numpy as np
import os

# --- 1. CONFIGURATION ---
KEY_LENGTH = 10000  # Longer key to handle file data (must be >= file size in bytes)
TAMPER_THRESHOLD = 0.05  # 5% QBER threshold
OUTPUT_FILENAME = "decrypted_file.txt" # The file Bob only creates if secure

# --- 2. BB84 PROTOCOL CLASSES (Simplified) ---

class Alice:
    """Simulates Alice preparing qubits for the quantum channel."""
    def __init__(self, length):
        self.bits = np.random.randint(2, size=length, dtype=np.uint8)
        self.bases = np.random.randint(2, size=length)
        self.qubits = self._encode_qubits()

    def _encode_qubits(self):
        # Qubit state is simulated as a tuple: (bit, basis)
        return list(zip(self.bits, self.bases))

class Bob:
    """Simulates Bob measuring the qubits and generating a key."""
    def __init__(self, length):
        self.bases = np.random.randint(2, size=length)
        self.measurements = []

    def measure(self, received_qubits):
        for i, (bit, alice_basis) in enumerate(received_qubits):
            if self.bases[i] == alice_basis:
                self.measurements.append(bit)
            else:
                self.measurements.append(np.random.randint(2, dtype=np.uint8))
        return np.array(self.measurements, dtype=np.uint8)

def eavesdropper_attack(qubits, attack_probability):
    """Simulates Eve's measurement, disturbing the quantum state (the 'touch')."""
    tampered_qubits = []
    eves_bits_stolen = 0
    for bit, basis in qubits:
        if np.random.rand() < attack_probability:
            # Eve's random measurement disturbs the state
            if np.random.randint(2) != basis:
                bit = 1 - bit  # Bit flip simulates collapse
            eves_bits_stolen += 1
        tampered_qubits.append((bit, basis))
    return tampered_qubits, eves_bits_stolen

def sift_and_check(alice_bases, bob_bases, alice_bits, bob_measurements):
    """Compares bases and checks the QBER for tampering detection."""
    matching_indices = np.where(alice_bases == bob_bases)[0]
    final_alice_key = alice_bits[matching_indices]
    final_bob_key = bob_measurements[matching_indices]

    errors = np.sum(final_alice_key != final_bob_key)
    qber = errors / len(final_bob_key) if len(final_bob_key) > 0 else 1.0

    return final_bob_key, qber

# --- 3. FILE ENCRYPTION/DECRYPTION FUNCTIONS ---

def file_to_bits(filename):
    """Reads file content and converts it to a flat numpy array of 0s and 1s."""
    with open(filename, 'rb') as f:
        file_bytes = f.read()

    # Convert bytes to a string of binary (0s and 1s), then to a numpy array
    bit_string = ''.join(format(byte, '08b') for byte in file_bytes)
    return np.array([int(bit) for bit in bit_string], dtype=np.uint8)

def bits_to_file(bit_array, output_filename):
    """Converts a numpy array of 0s and 1s back to file bytes."""
    # Ensure the array is a multiple of 8 bits (a whole number of bytes)
    if len(bit_array) % 8 != 0:
        raise ValueError("Bit array length is not a multiple of 8.")

    byte_list = []
    for i in range(0, len(bit_array), 8):
        byte_bits = bit_array[i:i+8]
        # Convert 8 bits to an integer, then to a byte
        byte_int = int("".join(map(str, byte_bits)), 2)
        byte_list.append(byte_int)

    with open(output_filename, 'wb') as f:
        f.write(bytes(byte_list))

def apply_otp(data_bits, key_bits):
    """Applies the One-Time Pad (XOR) operation."""
    # Key must be at least as long as the data. Use only the necessary key length.
    if len(key_bits) < len(data_bits):
        print("\n**ERROR: Key is too short for the file size! Key discarded.**")
        return None

    # XOR operation is the core of OTP encryption/decryption
    return data_bits[:len(data_bits)] ^ key_bits[:len(data_bits)]


# --- 4. THE FULL WORKFLOW ---

def secure_file_transfer(attack_prob, input_path, delete_on_tamper=True):
    """The full QKD and file transfer process with tamper-loss enforcement for a single file."""

    # Load and convert the file to bits
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found. Please create it first.")
        return None

    file_data_bits = file_to_bits(input_path)

    # A. QKD (Key Generation)
    # Ensure KEY_LENGTH is at least as long as the file data in bits
    dynamic_key_length = max(KEY_LENGTH, len(file_data_bits))

    alice = Alice(dynamic_key_length)
    tampered_qubits, eves_bits_stolen = eavesdropper_attack(alice.qubits, attack_prob)
    bob = Bob(dynamic_key_length)
    bob_measurements = bob.measure(tampered_qubits)
    secret_key, qber = sift_and_check(alice.bases, bob.bases, alice.bits, bob_measurements)

    print(f"\n--- QKD AUDIT for {input_path} ---")
    print(f"File Size (Bits): {len(file_data_bits)}")
    print(f"Key Length After Sifting: {len(secret_key)}")
    print(f"Quantum Bit Error Rate (QBER): {qber:.4f} ({qber * 100:.2f}%)")
    print("-" * 20)

    # B. Tamper-Detection and Data Loss Mechanism (Your Requirement)
    if qber > TAMPER_THRESHOLD:
        print("🚨 **TAMPERING DETECTED!** QBER exceeds the security threshold.")
        # Key is discarded, and the file is **NOT SENT/DECRYPTED**.
        print(f"The file data **DISAPPEARS** (is lost) at Bob's end.")
        if delete_on_tamper and os.path.exists(input_path):
            os.remove(input_path)
            print(f"Original file '{input_path}' has been deleted due to detected tampering.")
        elif not delete_on_tamper:
            print(f"Original file '{input_path}' was NOT deleted as 'nodelete' flag was set.")
        return False
    else:
        print("✅ **CHANNEL IS SECURE.** Proceeding with encryption.")

        # C. Secure Encapsulation (Encryption using the QKD key)
        # Note: In a real system, Alice would do the encryption. Here, we simulate the
        # XOR with a matching, uncorrupted key at the start for simplicity.

        # Ensure the sifted key is long enough for the file data
        if len(secret_key) < len(file_data_bits):
             print("\n**ERROR: The generated sifted key is too short for the file data. Aborting.**")
             return False

        # C. Secure Encapsulation (Encryption using the QKD key)
        # Note: In a real system, Alice would do the encryption. Here, we simulate the
        # XOR with a matching, uncorrupted key at the start for simplicity.

        # Use Alice's version of the key to encrypt (simulate Alice sending ciphertext)
        # Ensure Alice's key portion is also long enough
        alice_key_for_encryption = alice.bits[:len(file_data_bits)]
        if len(alice_key_for_encryption) < len(file_data_bits):
            print("\n**ERROR: Alice's key portion is too short for encryption. Aborting.**")
            return False

        ciphertext_bits = apply_otp(file_data_bits, alice_key_for_encryption)

        if ciphertext_bits is None: # Check if apply_otp failed
            print("\n**ERROR: Encryption failed due to key length issue. Aborting.**")
            return False

        # D. Decryption (Bob receives the ciphertext and decrypts with HIS key)
        decrypted_bits = apply_otp(ciphertext_bits, secret_key)

        if decrypted_bits is None: # Check if apply_otp failed
            print("\n**ERROR: Decryption failed due to key length issue. Aborting.**")
            return False

        # E. Reassemble the file
        bits_to_file(decrypted_bits, OUTPUT_FILENAME)

        print(f"File successfully received, decrypted, and saved as '{OUTPUT_FILENAME}'")
        return True

def secure_folder_transfer(attack_prob, input_directory, delete_on_tamper=True):
    """Iterates through files in a directory and applies secure_file_transfer."""
    if not os.path.isdir(input_directory):
        print(f"Error: Directory '{input_directory}' not found.")
        return False

    print(f"\n--- Initiating secure transfer for folder: '{input_directory}' ---")
    all_transfers_successful = True
    for root, _, files in os.walk(input_directory):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"\nProcessing file: {file_path}")
            success = secure_file_transfer(attack_prob, file_path, delete_on_tamper)
            if not success:
                all_transfers_successful = False
    print(f"\n--- Folder transfer for '{input_directory}' complete ---")
    return all_transfers_successful

# --- EXECUTION ---

# Remove old decrypted file to prove successful creation on secure transfer
if os.path.exists(OUTPUT_FILENAME):
    os.remove(OUTPUT_FILENAME)

# The execution block is removed as it will now be handled by the API layer and Gradio.
# This file will now primarily serve as a module.
