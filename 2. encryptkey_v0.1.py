import os
import random
import string
from cryptography.fernet import Fernet

# Function to load the encryption key
# Make sure the "secret.key" file is generated using a key generation script (e.g., generatekey.py)
def load_key():
    return open("secret.key", "rb").read()  # <--- Ensure "secret.key" exists in the same directory

# Function to encrypt the password using the encryption key
def encrypt_password(password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Function to replace the plaintext password in the script with an encrypted one
# This will search for the line containing 'my_password =' and replace the password
def overwrite_password_in_script(script_path, new_password):
    with open(script_path, 'r') as file:
        script_lines = file.readlines()

    # Find the line containing the password and replace it
    for i, line in enumerate(script_lines):
        if line.strip().startswith("my_password ="):
            # Replace with the scrambled password
            script_lines[i] = f'my_password = "{new_password}"  # Password has been scrambled\n'
            break

    # Write the updated lines back to the script
    with open(script_path, 'w') as file:
        file.writelines(script_lines)

# Encrypt the provided password
# Update 'my_password' with your real password before running the script
my_password = "*d<fsgPcRl"  # <--- Replace with your actual password before running
encrypted_password = encrypt_password(my_password)
print("Encrypted password:", encrypted_password)

# Scramble the original password or replace it with a random string
# This ensures the original password is not stored in the script
scrambled_password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(my_password)))

# Get the current script file path
script_path = os.path.abspath(__file__)  # Automatically gets the path of this script

# Overwrite the password in the script with the scrambled version
overwrite_password_in_script(script_path, scrambled_password)
