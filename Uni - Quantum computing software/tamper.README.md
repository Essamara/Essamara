# Quantum Key Distribution (QKD) Secure File Transfer (`tamper.py`)

This script simulates a secure file transfer using the BB84 Quantum Key Distribution (QKD) protocol. It demonstrates a key feature of quantum communication: the ability to detect eavesdropping. If tampering is detected, the transfer is aborted, and the data is considered lost.

## Description

This script provides a simulation of a secure communication channel protected by the laws of quantum mechanics. It implements the following concepts:

-   **BB84 Protocol**: The core of the script is a simplified simulation of the BB84 QKD protocol.
    -   **Alice**: The sender, who encodes bits onto qubits using random bases.
    -   **Bob**: The receiver, who measures the qubits using his own random bases.
    -   **Eve**: An eavesdropper, who attempts to intercept and measure the qubits, inevitably disturbing their state.
-   **Quantum Bit Error Rate (QBER)**: After the quantum transmission, Alice and Bob compare a subset of their bases to calculate the QBER. A high QBER indicates the presence of an eavesdropper.
-   **Tamper-Loss Mechanism**: If the QBER exceeds a predefined threshold (5% by default), the key is discarded, and the file is not "sent." This simulates the "loss" of data in a tampered channel.
-   **One-Time Pad (OTP) Encryption**: If the channel is deemed secure, the generated quantum key is used to encrypt and decrypt the file using the unbreakable OTP cipher.

## Dependencies

-   **Python 3.x**
-   **NumPy**: For numerical operations.

You can install NumPy using pip:
```bash
pip install numpy
```

## How It Works

The `secure_file_transfer` function orchestrates the entire process:

1.  **File Conversion**: The input file is converted into a stream of bits.
2.  **QKD Simulation**: The BB84 protocol is simulated to generate a secret key between Alice and Bob. The simulation includes a potential eavesdropper whose interference is controlled by an `attack_probability`.
3.  **Tampering Detection**: The QBER is calculated. If it's above the threshold, the transfer is aborted.
4.  **Encryption and Decryption**: If the channel is secure, the file data is encrypted with the quantum key (using a bitwise XOR operation), and then decrypted by the receiver.
5.  **File Reconstruction**: The decrypted bits are converted back into a file.

## How to Run

The script is designed to be used as a module. You can import the `secure_file_transfer` or `secure_folder_transfer` functions into your own Python code to simulate a secure transfer.

### Example Usage

```python
from tamper import secure_file_transfer, secure_folder_transfer

# Create a dummy file for the demonstration
with open("secret_data.txt", "w") as f:
    f.write("This is a secret message.")

# --- Scenario 1: No Eavesdropping ---
print("--- SIMULATING SECURE TRANSFER ---")
secure_file_transfer(attack_prob=0.0, input_path="secret_data.txt")

# --- Scenario 2: With Eavesdropping ---
print("\n--- SIMULATING TAMPERED TRANSFER ---")
secure_file_transfer(attack_prob=0.5, input_path="secret_data.txt")

# You can also transfer an entire folder
# secure_folder_transfer(attack_prob=0.1, input_directory="my_secure_folder")
```
When you run this example, you will see that in the secure scenario, a `decrypted_file.txt` is created. In the tampered scenario, the script will report that tampering was detected, and no decrypted file will be produced.
