import requests
import time
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os 
import msal
import pandas as pd
from cryptography.fernet import Fernet

from src.email_license.config.configuration import ConfigurationManager
from src.email_license import logger
from src.email_license.utils.auth import TokenManager
from src.email_license.extraction.license import LicenseExtractor

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Load the Fernet key
    fernet_key = os.getenv("FERNET_KEY")
    if not fernet_key:
        raise ValueError("FERNET_KEY is not set in the environment or .env file.")

    logger.info("Fernet key loaded")
    f = Fernet(fernet_key)

    logger.info("Initialize Configuration Manager")
    # Load API configurations
    config = ConfigurationManager()
    api_config = config.get_api_config()
    path_config = config.get_output_config()
    
    # config
    base_url = api_config.endpoint
    output_path = path_config.output_path
    
    logger.info("Initialize Token Manager")
    # Initialize TokenManager
    token_manager = TokenManager(
        api_config.client_id,
        f.decrypt(api_config.client_secret.encode()).decode(),
        api_config.authority,
        api_config.scope
    )

    # Initialize and Run License Extraction
    license_extractor = LicenseExtractor(token_manager, base_url, output_path,filename='O365_license')
    license_extractor.run()
