# Graph API Audit Logs Extraction

This project provides tools to extract audit logs from the Microsoft Graph API, process them, and store the results in CSV format for analysis.

## Features

- **Authentication**: Securely authenticate with the Microsoft Graph API using OAuth 2.0.
- **Audit Log Retrieval**: Fetch audit logs, including sign-in and directory audit logs.
- **Data Processing**: Process and filter logs to extract relevant information.
- **CSV Export**: Save processed logs into CSV files for easy analysis.

## Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Microsoft Entra ID (Azure AD)**: Access to an Azure AD tenant with appropriate permissions.
- **Microsoft Graph API Permissions**:
  - `AuditLog.Read.All`
  - `User.Read.All`

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jayyang17/GraphAPIAuditLogs.git
   cd GraphAPIAuditLogs

2. **Create a Virtual Environment and install the Dependencies**

3. **Configure Environment Variables: Set the following environment variables with your Azure AD**
    - CLIENT_ID
    - CLIENT_SECRET
    - TENANT_ID

4. **run the Extraction Script**:
    python main.py


## Usage
The fernet.py script is used to encrypt and update the client_secret in the config.yaml file when the secret changes. It ensures the updated secret is securely stored.

To use the encryption tool:

1. Run the fernet.py script:
    python src/encryption/fernet.py

2. Follow the prompts to input the new client_secret.

3. The fernet.py script will:
    Encrypt the new secret.
    Update the config.yaml file with the encrypted secret.
    This process ensures the client_secret remains secure while being accessible to the main application.


---

## Security

- The `client_secret` is encrypted using the `fernet.py` script and stored securely in `config.yaml`.
- Use environment variables, access-controlled directories, or vault services to protect sensitive files like `config.yaml`.
- Always ensure the encryption key is stored securely and accessible only to authorized personnel.

