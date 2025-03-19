import requests
import time
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os 
import msal
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

from src.email_license.config.configuration import ConfigurationManager
from src.email_license.utils.auth import TokenManager
from src.email_license.utils.common import save_to_csv
from src.email_license import logger

class LicenseExtractor:
    def __init__(self, token_manager, base_url, output_path, filename):
        self.token_manager = token_manager
        self.base_url = base_url
        self.output_path = output_path
        self.file_name = filename
    def fetch_all_users(self):
        """Fetch all users with extended properties including assigned licenses."""
        access_token = self.token_manager.get_access_token()

        headers = {"Authorization": f"Bearer {access_token}"}

        url = f"{self.base_url}/users?$select=id,displayName,assignedLicenses,mail,userPrincipalName,jobTitle,department,companyName,country,city,state,officeLocation,accountEnabled,creationType,signInActivity"

        users = []
        while url:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                users.extend(data.get("value", []))
                url = data.get("@odata.nextLink")  # Handle pagination
            else:
                logger.error(f"Error fetching users: {response.status_code} {response.text}")
                break
            
            time.sleep(1)  # Prevent rate limiting
        
        return users

    def fetch_sku_mapping(self):
        """Fetch all available license SKUs and their readable names."""
        access_token = self.token_manager.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        url = f"{self.base_url}/subscribedSkus"
        sku_mapping = {}

        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            for sku in response.json().get("value", []):
                sku_mapping[sku.get("skuId")] = sku.get("skuPartNumber")  # Example: "ENTERPRISEPACK" (E3)
        else:
            logger.error(f"Error fetching SKUs: {response.status_code} {response.text}")

        return sku_mapping

    def map_users_to_licenses(self, users, sku_mapping):
        """Map each user's assigned license SKU to readable names and return structured data."""
        mapped_users = []
        for user in users:
            assigned_licenses = user.get("assignedLicenses", [])

            # Convert license SKUs to readable names
            readable_licenses = [
                sku_mapping.get(lic.get("skuId"), f"Unknown SKU ({lic.get('skuId')})")
                for lic in assigned_licenses
            ]

            # Ensure every user has at least "None" if no licenses
            readable_licenses = readable_licenses if readable_licenses else ["None"]

            # Build a structured dictionary
            mapped_users.append({
                "User ID": user.get("id", "N/A"),
                "Display Name": user.get("displayName", "N/A"),
                "Email": user.get("mail", "N/A"),
                "UPN": user.get("userPrincipalName", "N/A"),
                "Job Title": user.get("jobTitle", "N/A"),
                "Department": user.get("department", "N/A"),
                "Company": user.get("companyName", "N/A"),
                "Country": user.get("country", "N/A"),
                "City": user.get("city", "N/A"),
                "State": user.get("state", "N/A"),
                "Office Location": user.get("officeLocation", "N/A"),
                "Account Enabled": user.get("accountEnabled", "N/A"),
                "Creation Type": user.get("creationType", "N/A"),
                "Last Sign-In": user.get("signInActivity", {}).get("lastSignInDateTime", "Never"),
                "License Type": ", ".join(readable_licenses)
            })

        return mapped_users

    def run(self):
        logger.info("Fetching user properties")
        users = self.fetch_all_users()

        logger.info("Fetch all available license SKUs")
        sku_mapping = self.fetch_sku_mapping()

        logger.info("Mapping each user's assigned license SKU")
        mapped_users = self.map_users_to_licenses(users, sku_mapping)

        logger.info("Saving file...")
        save_to_csv(mapped_users,self.output_path,self.file_name)

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Load the Fernet key
    fernet_key = os.getenv("FERNET_KEY")
    if not fernet_key:
        raise ValueError("FERNET_KEY is not set in the environment or .env file.")
    logger.info("Fernet key loaded")

    f = Fernet(fernet_key)

    # Load API configurations
    config = ConfigurationManager()
    api_config = config.get_api_config()
    path_config = config.get_output_config()
    
    # config
    base_url = api_config.endpoint
    output_path = path_config.output_path

    # Initialize TokenManager
    token_manager = TokenManager(
        api_config.client_id,
        f.decrypt(api_config.client_secret.encode()).decode(),
        api_config.authority,
        api_config.scope
    )

    # Initialize and Run License Extraction
    license_extractor = LicenseExtractor(token_manager, api_config.endpoint, output_path,filename='O365_license')
    license_extractor.run()
