# gisenterprisereporter_scheduler
This script is in response to https://github.com/dannykrouk/gisenterprisereporter, for GISAdmins. BLUF: The script is made to run CLI for GIS Enterprise Reporter Tool, place the report in the folder of choosing, and send a email when done. 

Prerequisites for Running These Scripts

Before running the `generatekey.py`, `encryptkey.py`, and `gis_enterprise_reporter_v0.1.py` scripts, you need to ensure that your environment is properly set up. Below are the prerequisites for each script:


**1. General Prerequisites (For All Scripts)**

 a. **Python Installation:
- Make sure you have **Python 3.6+** installed. You can download it from the [official Python website](https://www.python.org/downloads/).

 b. Install Required Python Libraries:
These scripts use the `cryptography` library, which needs to be installed. You can install it using `pip`:

pip install cryptography

 c. Set Up Environment:
- Create a folder where you’ll store all related scripts and files (e.g., `gis_enterprise_reporter`).
- Ensure all scripts are placed in the same folder for easier access to shared files (e.g., `secret.key`).

**2. Script-Specific Prerequisites**

 1. generatekey.py

This script generates an encryption key used to secure sensitive information like passwords.

Steps to prepare:
- No specific setup required before running this script. It will create a `secret.key` file.
  
What it does:
- This script generates a file named `secret.key`, which will be used by other scripts to encrypt and decrypt data.

Run it once before running the other scripts:

python generatekey.py

 2. encryptkey.py

This script encrypts sensitive information (like passwords) using the `secret.key` generated by `generatekey.py`.

Steps to prepare:
- Ensure the `secret.key` file has been generated by running the `generatekey.py` script.
- Open the script and update the `my_password` variable with your actual password. 

What it does:
- This script will encrypt a given password using the key stored in `secret.key`, scramble the password, and replace it in the script file.

 3. gis_enterprise_reporter_v0.1.py

This script runs the GIS Enterprise Reporter tool, moves the output files, and sends email notifications.

Steps to prepare:
- GIS Enterprise Reporter Tool: Make sure the GIS Enterprise Reporter executable (`er.exe`) and its configuration file (`er.config`) are available and configured correctly.
- secret.key: Ensure that the `secret.key` file has been generated using `generatekey.py` and placed in the correct path.
- Email SMTP Configuration: Ensure that your environment has access to an SMTP server for sending emails. Update the email parameters in the script.

What it does:
- This script decrypts a password stored in `er.config`, runs the Enterprise Reporter tool, moves the output files to a designated directory, and sends a notification email.

**3. File Structure**

Ensure that your folder structure looks something like this:

gis_enterprise_reporter/
│
├── generatekey.py                # Run this script first to generate the encryption key
├── encryptkey.py                 # Script to encrypt passwords
├── gis_enterprise_reporter_v0.1.py   # Main reporter script
├── secret.key                    # Generated key file (after running generatekey.py)
├── er.exe                        # GIS Enterprise Reporter tool
├── er.config                     # GIS Enterprise Reporter config file
└── (other dependencies)

**4. Running the Scripts**

1. Run `generatekey.py` to create the `secret.key` file:

python generatekey.py

2. Run `encryptkey.py` to encrypt passwords:

python encryptkey.py

3. Run `gis_enterprise_reporter_v0.1.py` to generate reports and send emails:

python gis_enterprise_reporter_v0.1.py

**5. Other Considerations**

- Permissions: Ensure that you have the necessary permissions to access the directories and files mentioned in the scripts.
- SMTP Access: If you're sending emails, ensure that you have access to a working SMTP server and the correct credentials.
- Backup: Always keep a backup of sensitive data before running any scripts that manipulate files.

With these prerequisites in place, you should be ready to run all the scripts without issues. Let me know if you need any further details!

1. generatekey.py​
This script is responsible for generating an encryption key that can later be used to encrypt and decrypt sensitive information such as passwords.

Key Functions:
generate_key(): This function generates a new encryption key using the cryptography.fernet library and saves it to a file named secret.key. This key will be used for encryption and decryption in other scripts.
Purpose: This script is typically run once to create the key file, which is stored securely and used in other processes requiring encryption.

2. encryptkey.py​
This script is designed to encrypt a plaintext password using the encryption key generated by generatekey.py.

Key Functions:
load_key(): Loads the encryption key stored in the secret.key file.
encrypt_password(): Encrypts a given plaintext password using the key loaded by load_key().
overwrite_password_in_script(): Searches for the password in a script file and replaces it with an encrypted or scrambled version.
Process:

First, the script encrypts the password my_password.
Then, it scrambles the plaintext password with a random string of the same length.
Finally, it searches for the password in the current script and replaces it with the scrambled version, ensuring no plaintext passwords remain in the code.
Purpose: This script helps protect sensitive information by encrypting and scrambling plaintext passwords in scripts, thus improving security by preventing exposed credentials.

3. gis_enterprise_reporter_v0.1.py
This script manages the execution of the "GIS Enterprise Reporter" tool, which generates reports about an ArcGIS Enterprise system, including detailed configuration information, status, and usage.

Key Functions:
Password Management:
decrypt_password(): Decrypts the password stored in the configuration file (er.config) using the key generated in generatekey.py.
decrypt_config_password(): Loads and decrypts the password stored in the configuration file, ensuring the password is secure and only decrypted just before use.
Tool Execution:
run_er_tool(): Decrypts the password, temporarily updates the configuration file with the decrypted password, runs the GIS Enterprise Reporter tool (er.exe), and then cleans up temporary files.
File Management:
move_output_files(): Moves the generated report files to a target directory, automatically creating folders based on the current year, month, and day.
Email Notification:
send_email(): Sends an email to notify relevant recipients that the report has been generated successfully.
