from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DockerIgnoreConfig:
    python_cache: bool = True,
    virtual_environment: bool = True,
    system_spec_files: bool = True,
    logs: Optional[bool] = False,
    test_coverage: bool = True,
    git: Optional[bool] = False,
    docker: Optional[bool] = False,
    poetry: Optional[bool] = False,
    compiled_files: bool = True,
    documentation: bool = True,
    env_files: Optional[bool] = False,