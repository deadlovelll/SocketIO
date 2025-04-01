from dataclasses import dataclass, field
import requests

from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_validator.pre_commit_hooks_validator import PreCommitHooksValidator

@dataclass
class BlackConfig:
    url: str = field (
        init=False, 
        default='https://github.com/psf/black'
    )
    rev: str = field (
        default_factory=lambda: BlackConfig.get_latest_version()
    )
    line_length: str
    target_version: str
    skip_string_normalization: bool
    check: bool
    diff: bool
    
    @staticmethod
    def get_latest_version() -> str:
        pass
    
    def __post_init__ (
        self,
    ) -> None:
        
        pass