# Quantum-Enhanced File Encryption (`encryptqfile.py`)

This script demonstrates an advanced cryptographic process: encrypting and decrypting a file using the AES-256 GCM algorithm, with an encryption key generated from a quantum random number generator (QRNG).

## Description

This script provides a practical example of post-quantum cryptography principles by securing a file with a key that originates from a quantum source. This method enhances security by using a truly unpredictable and non-deterministic seed for the encryption key.

The script performs a full encryption/decryption cycle:
1.  **Quantum Key Generation**: It uses a Qiskit-based quantum circuit to generate 256 bits of high-quality random data.
2.  **Key Derivation**: The raw quantum bits are then processed through the SHAKE-256 hash function to produce a secure and uniform 256-bit (32-byte) key.
3.  **File Encryption**: The generated key is used to encrypt a specified file (`image.png` by default) using AES-256 in Galois/Counter Mode (GCM). GCM is an authenticated encryption mode that ensures both data confidentiality and integrity.
4.  **File Decryption**: The script then uses the same quantum-derived key to decrypt the file, verifying its integrity in the process.

## Dependencies

- **Python 3.x**
- **Qiskit**: An open-source framework for quantum computing.
- **Cryptography**: A Python library providing cryptographic recipes and primitives.

You can install the required libraries using pip:
```bash
pip install qiskit cryptography
```

## How to Run

1.  Place a file named `image.png` in the same directory as the script. If the file does not exist, a dummy text file will be created in its place for the demonstration.
2.  Execute the script from your terminal:
    ```bash
    python encryptqfile.py
    ```

The script will perform the following actions:
- Generate a 256-bit key from the QRNG.
- Encrypt `image.png` and save the result as `image.png.enc`.
- Decrypt `image.png.enc` and save the result as `image_decrypted.png`.

You can then compare the original `image.png` with `image_decrypted.png` to verify that the process was successful.
