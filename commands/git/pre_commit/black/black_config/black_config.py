from dataclasses import dataclass, field

from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_validator.pre_commit_hooks_validator import PreCommitHooksValidator
from commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher

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
        
    def __post_init__ (
        self,
    ) -> None:
        
        owner_repo = self.url.split("https://github.com/")[1]
        self.rev = LastReleaseFetcher.fetch(owner_repo)