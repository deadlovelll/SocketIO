import sys

from dataclasses import dataclass, field

from commands.git.pre_commit.black.black_validator.black_validator import BlackValidator
from commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher

@dataclass
class BlackConfig:
    url: str = field (
        init=False, 
        default='https://github.com/psf/black',
    )
    rev: str = None
    line_length: int = 88
    target_version: str = None
    skip_string_normalization: bool = True
    skip_magic_trailing_comma: bool = False
    check: bool = True
    diff: bool = True
    preview: bool = True             
    verbose: bool = False
    quiet: bool = False             
    fast: bool = True
        
    def __post_init__ (
        self,
    ) -> None:
        
        if not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo)
        else:
            BlackValidator.verify_black_version(self.rev)  
            
        if not self.target_version:
            py_version = sys.version_info
            self.target_version = f'py{py_version.major}{py_version.minor}'
            