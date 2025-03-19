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

        # Initialize the config manager
        config = ConfigurationManager()
        api_config = config.get_api_config()

        # Update the client secret 
        updated_api_config = api_config
        updated_api_config.client_secret = encrypted_password

        config.update_api_config(updated_api_config)
        
        print("Password encrypted and YAML file updated successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()