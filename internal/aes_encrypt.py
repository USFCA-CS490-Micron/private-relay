from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

# AES encrypt string
def aes_encrypt(data: str, key: str) -> str:
    """
    Encrypt a string using AES
    :param data: Original string
    :param key: Encryption key (16/24/32 bytes)
    :return: Encrypted Base64 string
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
    iv = cipher.iv  # Initialization vector
    encrypted = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + encrypted).decode('utf-8')

# AES decrypt string
def aes_decrypt(encrypted_data: str, key: str) -> str:
    """
    Decrypt a string using AES
    :param encrypted_data: Encrypted Base64 string
    :param key: Encryption key (16/24/32 bytes)
    :return: Decrypted string
    """
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv = encrypted_data_bytes[:AES.block_size]
    encrypted = encrypted_data_bytes[AES.block_size:]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode('utf-8')

# Encrypt image
def encrypt_image(image_path: str, key: bytes, output_path: str) -> None:
    """
    Encrypt an image using AES
    :param image_path: Path to the image to be encrypted
    :param key: Encryption key (16/24/32 bytes)
    :param output_path: Path to save the encrypted file
    """
    with open(image_path, 'rb') as f:
        image_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))

    with open(output_path, 'wb') as f:
        f.write(iv + encrypted_data)

    print(f"Image encryption completed, saved to {output_path}")

# Decrypt image
def decrypt_image(encrypted_path: str, key: bytes, output_path: str) -> None:
    """
    Decrypt an encrypted image using AES
    :param encrypted_path: Path to the encrypted image
    :param key: Encryption key (16/24/32 bytes)
    :param output_path: Path to save the decrypted file
    """
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()

    iv = encrypted_data[:AES.block_size]
    encrypted = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted), AES.block_size)

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

    print(f"Image decryption completed, saved to {output_path}")

# Example usage
if __name__ == "__main__":
    key = "thisisasecretkey"  # Key must be 16/24/32 bytes
    original = "hello world123123adawdwa1111"

    # String encryption and decryption
    encrypted = aes_encrypt(original, key)
    print(f"Encrypted: {encrypted}")

    decrypted = aes_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")

    # Image encryption and decryption
    #image_key = b"thisisasecretkey"  # Key in bytes format
    #encrypt_image("example.jpg", image_key, "encrypted_image.dat")
    #decrypt_image("encrypted_image.dat", image_key, "decrypted_image.jpg")
