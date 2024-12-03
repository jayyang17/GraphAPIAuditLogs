from src.email_license import logger
from src.email_license.extraction.extraction import authenticate_graph_api, fetch_audit_logs, save_logs_to_csv

if __name__=="__main__":
    try:
        logger.info("Authenticating with MS Graph API")
        token = authenticate_graph_api()

        logger.info("Fetching audit logs...")
        audit_logs = fetch_audit_logs(token)

        save_logs_to_csv(audit_logs)
    except Exception as e:
        logger.info(f"An error occured at {e}")

