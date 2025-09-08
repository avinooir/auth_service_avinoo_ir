#!/usr/bin/env python
"""
Script to generate RSA keys for JWT signing
"""

import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_rsa_keys():
    """Generate RSA private and public keys for JWT signing."""
    
    # Create keys directory if it doesn't exist
    keys_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'keys')
    os.makedirs(keys_dir, exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Serialize private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Write private key to file
    private_key_path = os.path.join(keys_dir, 'private_key.pem')
    with open(private_key_path, 'wb') as f:
        f.write(private_pem)
    
    # Write public key to file
    public_key_path = os.path.join(keys_dir, 'public_key.pem')
    with open(public_key_path, 'wb') as f:
        f.write(public_pem)
    
    print(f"✅ RSA keys generated successfully!")
    print(f"Private key: {private_key_path}")
    print(f"Public key: {public_key_path}")
    print(f"Key size: 2048 bits")
    print(f"Algorithm: RS256")

if __name__ == '__main__':
    generate_rsa_keys()
