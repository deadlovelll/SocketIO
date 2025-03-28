from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DockerfileConfig:
    filename: str = "Dockerfile"
    python_version: str = "latest"
    use_alpine: bool = False
    install_system_deps: bool = True
    poetry: bool = True
    ports: List[int] = field(default_factory=lambda: [4000])
    entrypoint: str = "main.py"
    use_nonroot_user: bool = True
    grpc_enabled: bool = False
    in_env: bool = False
    os_type: Optional[str] = None