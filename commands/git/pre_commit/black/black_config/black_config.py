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
    line_length: str
    target_version: str
    skip_string_normalization: bool
    check: bool
    diff: bool
        
    def __post_init__ (
        self,
    ) -> None:
        
        if not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo)
        else:
            BlackValidator.verify_black_version(self.rev)