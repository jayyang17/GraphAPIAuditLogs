import os
import msal
from msal import PublicClientApplication, ConfidentialClientApplication
import requests
import os
import json
import pandas as pd

from src.email_license.constants import *
from src.email_license.utils.common import read_yaml
from src.email_license.config.configuration import ConfigurationManager
from src.email_license import logger


# get the credentials from config
config = ConfigurationManager()
api_config = config.get_api_config()
CLIENT_ID = api_config.client_id
CLIENT_SECRET = api_config.client_secret
TENANT_ID = api_config.tenant_id
base_url = api_config.endpoint
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['https://graph.microsoft.com/.default']

# get the path from config
path_config = config.get_output_config()
output_path = path_config.rootdir
shared_path = path_config.shared_path

def authenticate_graph_api():
    access_token = None

    # default_scope = 'https%3A%2F%2Fgraph.microsoft.com%2F.default'
    # grant_type = 'client_credentials'

    try:
        client_instance = msal.ConfidentialClientApplication(
            client_id = CLIENT_ID,
            client_credential = CLIENT_SECRET,
            authority = AUTHORITY,
        )

        logger.info("Create client instance..... Call MSAL library")

        token_response = client_instance.acquire_token_for_client(scopes=SCOPE)

        if 'access_token' in token_response:
            access_token = token_response['access_token']
            return access_token
        else:
            print("Error acquiring token:", token_response.get("error_description"))
    except Exception as e:
        logger.info("Error during authentication with MS GRAPH API")

# Fetch audit logs from Graph API
def fetch_audit_logs(access_token):
    endpoint = f"{base_url}/auditLogs/signIns"
    headers = {"Authorization": f"Bearer {access_token}"}
    logs = []
    
    while endpoint:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            data = response.json()
            logs.extend(data.get("value", []))
            endpoint = data.get("@odata.nextLink", None)  # Handle pagination
        else:
            logger.info(f"Error fetching audit logs: {response.status_code} {response.text}")
            break
    return logs

# Save logs to a CSV file
def save_logs_to_csv(logs):
    if logs:
        df = pd.DataFrame(logs)
        # save to this package
        df.to_csv(output_path, index=False)
        logger.info(f"Audit logs saved to {output_path}")

        # save to shared folder
        df.to_csv(shared_path, index=False)
        logger.info(f"Audit logs saved to {shared_path}")
    else:
        logger.info("No logs available to save.")

