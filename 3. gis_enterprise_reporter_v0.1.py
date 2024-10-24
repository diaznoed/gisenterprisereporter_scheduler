# Version 0.1: 10/24/2024
# Created By: Noe Diaz

import os
import subprocess
import shutil
import smtplib
import json
from email.message import EmailMessage
from cryptography.fernet import Fernet
from datetime import datetime

# Paths (Users should update these to match their environment)
# Path to the GIS Enterprise Reporter executable
exe_path = r"F:\Path\To\Your\er.exe"  # <--- Update this path

# Path to the GIS Enterprise Reporter configuration file
config_file = r"F:\Path\To\Your\er.config"  # <--- Update this path

# Path to the output directory where the reports are generated
output_dir = r"F:\Path\To\Your\Output\Directory"  # <--- Update this path

# Path to where the reports should be moved
target_directory = r"\\Path\To\Your\Target\Directory\2024\9. September"  # <--- Update this path

# Path to the secret key file for decryption
secret_key_path = r"F:\Path\To\Your\secret.key"  # <--- Update this path

# Email parameters (Users should update these with their own email details)
email_subject = "GeoState Enterprise Report"  # <--- Update the subject line if needed
email_body = ("The GIS Enterprise Weekly Report is complete, the output is located in the "
              "\\Path\\To\\Report\\2024\n\n"  # <--- Update this path
              "Please review anything necessary.\n\n"
              "Thanks -GeoState.")
from_address = "youremail@example.com"  # <--- Update this with your email address
to_addresses = ["recipient1@example.com", "recipient2@example.com"]  # <--- Add recipients
smtp_server = "your.smtp.server.com"  # <--- Update with your SMTP server

# Function to load the encryption key
def load_key():
    return open(secret_key_path, "rb").read()

# Function to decrypt the password
def decrypt_password(encrypted_password):
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Step 1: Decrypt the password just before running the tool
def decrypt_config_password():
    with open(config_file, 'r') as file:
        config_data = json.load(file)

    # Decrypt the password
    encrypted_password = config_data["AdminPassword"].encode()
    decrypted_password = decrypt_password(encrypted_password)

    # Return decrypted password without saving it back to the config file
    return decrypted_password

# Step 2: Call the er.exe tool
def run_er_tool():
    try:
        # Decrypt the password before running
        decrypted_password = decrypt_config_password()

        # Load config data
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        # Temporarily update the password in memory (but not the file)
        config_data["AdminPassword"] = decrypted_password

        # Save the config temporarily for running the tool
        temp_config_file = config_file + ".temp"
        with open(temp_config_file, 'w') as file:
            json.dump(config_data, file, indent=4)

        # Run the tool using the temporary config file
        subprocess.run([exe_path, temp_config_file], check=True)

        # Remove temporary config file after running
        os.remove(temp_config_file)
        
        print("GIS Enterprise Reporter executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running GIS Enterprise Reporter: {e}")

# Step 3: Send an email notification
def send_email():
    msg = EmailMessage()
    msg["Subject"] = email_subject
    msg["From"] = from_address
    msg["To"] = ", ".join(to_addresses)
    msg.set_content(email_body)

    # Send the email
    with smtplib.SMTP(smtp_server) as server:
        server.send_message(msg)
        print("Email sent successfully.")

# Step 4: Move the output files to the target directory
def move_output_files():
    # Get the current year, month, and day
    current_year = datetime.now().strftime("%Y")
    current_month_number = datetime.now().strftime("%m")
    current_month_name = datetime.now().strftime("%B")
    current_day = datetime.now().strftime("%d")
    
    # Create the month folder with the format "09. September"
    month_folder = f"{current_month_number}. {current_month_name}"
    
    # Set the target directory structure
    year_folder_path = os.path.join(r"\\Path\\To\\Target\\Directory\\Enterprise Reporter", current_year)  # <--- Update this path
    month_folder_path = os.path.join(year_folder_path, month_folder)
    
    # Check if the year and month folders exist; if not, create them
    if not os.path.exists(year_folder_path):
        os.makedirs(year_folder_path)
    if not os.path.exists(month_folder_path):
        os.makedirs(month_folder_path)
    
    # Create the day folder (e.g., "2024-09-01") inside the month folder
    day_folder = datetime.now().strftime("%Y-%m-%d")
    target_folder = os.path.join(month_folder_path, day_folder)
    
    # Create the day folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Move files from output directory to the target directory
    for filename in os.listdir(output_dir):
        src = os.path.join(output_dir, filename)
        dst = os.path.join(target_folder, filename)
        shutil.move(src, dst)
        print(f"Moved {filename} to {target_folder}")

# Main function to execute the entire process
def main():
    run_er_tool()  # Step 1: Run the tool
    move_output_files()  # Step 2: Move the generated report files
    send_email()  # Step 3: Send email notification

# Run the script
if __name__ == "__main__":
    main()
