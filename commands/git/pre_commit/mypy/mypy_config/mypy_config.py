from dataclasses import dataclass, field
from typing import Optional

from commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher

@dataclass
class MypyConfig:
    url: str = field(init=False, default='https://github.com/python/mypy')
    rev: str = None

    config_file: Optional[str] = 'mypy.ini' 
    python_version: Optional[str] = None     
    ignore_missing_imports: bool = True
    disallow_untyped_defs: bool = False
    strict_optional: bool = False
    check_untyped_defs: bool = True
    no_implicit_optional: bool = False
    show_error_codes: bool = True
    warn_unused_ignores: bool = True
    exclude: Optional[str] = None

    def __post_init__ (
        self,
    ) -> None:
        
        if  not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo, True)