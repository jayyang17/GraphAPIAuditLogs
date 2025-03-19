from dataclasses import dataclass
from pathlib import Path

@dataclass
class OutputConfig:
    output_path: Path
    shared_path: Path
    
@dataclass
class ApiConfig:
    endpoint: str
    client_id: str
    client_secret: str
    tenant_id: str
    authority: str
    scope: list