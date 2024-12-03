from src.email_license.constants import *
from src.email_license.utils.common import * 
from src.email_license.config.configuration import ConfigurationManager
from src.email_license import logger

import os
import yaml
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pathlib import Path

def main():
    try:
        # Load environment variables
        load_dotenv()


        # Retrieve Fernet key from configuration
        # config = ConfigurationManager()
        # api_config = config.get_api_config()

        # encrypt_config = config.get_encrypt_config()
        # encrypt = encrypt_config.app_secret_key
        # print(encrypt)

        # Load the Fernet key
        fernet_key = os.getenv("FERNET_KEY")
        if not fernet_key:
            raise ValueError("FERNET_KEY is not set in the environment or .env file.")
        logger.info("Fernet key loaded")

        # Encode the key
        fernet = Fernet(fernet_key.encode())

        # Input the password to encrypt
        new_password = input("Enter the new password: ")
        logger.info("New password entered. Begining Encryption...")

        encrypted_password = fernet.encrypt(new_password.encode()).decode()


        # Update the YAML file
        config = read_yaml(CONFIG_FILE_PATH)

        # api_config.client_secret = encrypted_password
        config["graph_api"]["client_secret"] = encrypted_password
        
        # Read and update the existing YAML file
        write_yaml(config, CONFIG_FILE_PATH)

        print("Password encrypted and YAML file updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()