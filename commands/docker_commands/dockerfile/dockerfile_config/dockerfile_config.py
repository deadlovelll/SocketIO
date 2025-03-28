from dataclasses import dataclass, field
from typing import List, Optional

from commands.docker_commands.dockerfile.dockerfile_validator.dockerfile_validator import DockerfileValidator

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
    
    def __post_init__ (
        self,
    ) -> None:
        
        DockerfileValidator.verify_dockerfile_args (
            self.python_version,
            self.use_alpine,
            self.ports,
            self.entrypoint,
            self.grpc_enabled,
        )