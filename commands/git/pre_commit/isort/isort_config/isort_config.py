from dataclasses import dataclass, field
from typing import List, Optional

from commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher

@dataclass
class IsortConfig:
    url: str = field (
        init=False, 
        default='https://github.com/PyCQA/isort',
    )
    rev: str = None
    
    profile: str = 'black'
    check_only: bool = True
    diff: bool = True
    line_length: int = 88
    skip: Optional[List[str]] = field(default_factory=list)
    virtual_env: Optional[str] = None
    src: Optional[List[str]] = field(default_factory=list)
    float_to_top: bool = False
    
    profiles = [
        'black'
        'google'
        'pycharm'	
        'attrs'	
        'pep8'
    ]
    
    def __post_init__ (
        self,
    ) -> None:
        
        if not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo)