from src.email_license.constants import *
from src.email_license.utils.common import read_yaml, write_yaml
from src.email_license.config.config_entity import (ApiConfig, OutputConfig)

class ConfigurationManager:
    def __init__(self, 
                 config_filepath = CONFIG_FILE_PATH
                 ):
        self.config=read_yaml(config_filepath)
    
    def get_api_config(self) -> ApiConfig:
        config = self.config["graph_api"]

        api_config = ApiConfig(
            endpoint=config["endpoint"],
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            tenant_id=config["tenant_id"],
            authority=config["authority"].format(tenant_id=config["tenant_id"]),
            scope=config["scope"]
        )
        
        return api_config
    
    def get_output_config(self) -> OutputConfig:
        config = self.config["data_output"]

        output_config = OutputConfig(
            output_path=config["root_dir"],
            shared_path=config["shared_path"]
        )

        return output_config
    
    def update_api_config(self, updated_config: ApiConfig):
        """Update the API configuration in the YAML file"""
        self.config["graph_api"] ={
            "endpoint": updated_config.endpoint,
            "client_id": updated_config.client_id,
            "client_secret": updated_config.client_secret,
            "tenant_id": updated_config.tenant_id
        }
        write_yaml(self.config, CONFIG_FILE_PATH)


