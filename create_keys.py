#!/usr/bin/env python3
"""
تولید کلیدهای RSA برای JWT
"""

import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_rsa_keys():
    """تولید کلیدهای RSA"""
    print("🔑 تولید کلیدهای RSA...")
    
    # ایجاد دایرکتوری
    os.makedirs('keys', exist_ok=True)
    
    # تولید کلید
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    # ذخیره کلید خصوصی
    with open('keys/private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # ذخیره کلید عمومی
    with open('keys/public_key.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    print("✅ کلیدهای RSA تولید شدند!")
    print("📁 فایل‌ها:")
    print("   - keys/private_key.pem")
    print("   - keys/public_key.pem")

if __name__ == '__main__':
    generate_rsa_keys()
