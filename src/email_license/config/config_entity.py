from dataclasses import dataclass
from pathlib import Path

@dataclass
class OutputConfig:
    rootdir: Path
    shared_path: Path

class ApiConfig:
    endpoint: str
    client_id: str
    client_secret: str
    tenant_id: str
