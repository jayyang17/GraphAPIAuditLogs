import os
import time
import msal
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from src.email_license.config.configuration import ConfigurationManager
from src.email_license import logger

class TokenManager:
    def __init__(self, client_id, client_secret, authority, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = authority
        self.scope = scope
        self.access_token = None
        self.expiry = 0

    def get_access_token(self):
        """Returns a valid access token, refreshing if expired."""
        if not self.access_token or time.time() >= self.expiry:
            self.refresh_token()
        return self.access_token

    def refresh_token(self):
        """Fetch a new token from Microsoft Graph API."""
        try:
            client_instance = msal.ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=self.authority
            )

            logger.info("Creating client instance... Calling MSAL library")

            token_response = client_instance.acquire_token_for_client(scopes=self.scope)

            if 'access_token' in token_response:
                self.access_token = token_response['access_token']
                self.expiry = time.time() + token_response.get("expires_in", 3600) - 300  # Refresh 5 min before expiry
                logger.info(f"Access token obtained. Expires at {self.expiry}")
            else:
                logger.error(f"Error acquiring token: {token_response.get('error_description')}")
                raise Exception("Token acquisition failed.")
        except Exception as e:
            logger.error(f"Error during authentication with MS GRAPH API: {str(e)}")
            raise

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    # Load the Fernet key
    fernet_key = os.getenv("FERNET_KEY")
    if not fernet_key:
        raise ValueError("FERNET_KEY is not set in the environment or .env file.")
    logger.info("Fernet key loaded")

    f = Fernet(fernet_key)

    # Get credentials from config
    config = ConfigurationManager()
    api_config = config.get_api_config()
    CLIENT_ID = api_config.client_id
    ENCRYPTED_CLIENT_SECRET = api_config.client_secret
    CLIENT_SECRET = f.decrypt(ENCRYPTED_CLIENT_SECRET.encode()).decode()
    TENANT_ID = api_config.tenant_id
    base_url = api_config.endpoint
    AUTHORITY = api_config.authority
    SCOPE = api_config.scope

    token_manager = TokenManager(CLIENT_ID, CLIENT_SECRET, AUTHORITY, SCOPE)

    # Don't store token, always fetch dynamically
    print("Access Token:", token_manager.get_access_token())
