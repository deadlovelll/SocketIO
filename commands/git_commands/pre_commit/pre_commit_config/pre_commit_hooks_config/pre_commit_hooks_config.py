from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PreCommitHooksConfig:
    url: str = 'https://github.com/pre-commit/pre-commit-hooks'
    rev: str
    
    def __post_init__ (
        self,
    ) -> None:
        
        pass