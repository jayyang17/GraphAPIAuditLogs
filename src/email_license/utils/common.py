import os 
import yaml
from src.email_license import logger
import json
import joblib
from ensure import ensure_annotations
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path):
    """reads yaml file and return

    Args:
        path_to_yaml (str): path input
    
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    
    Returns:
        ConfigBox: ConfigBox type

    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded succesfully")
            return content
        
    except ValueError:
        raise ValueError("yaml file is empty")
    
    except Exception as e:
        raise e

@ensure_annotations
def write_yaml(data, path_to_yaml: Path):
    """
    Writes data to a YAML file.
    """
    try:
        with open(path_to_yaml, "w") as file:
            yaml.dump(data, file, default_flow_style=False)
            logger.info(f"yaml file updated")
    except ValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


