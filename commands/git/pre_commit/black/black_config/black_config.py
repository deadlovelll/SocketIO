"""
Black configuration dataclass with automatic version resolution and validation.

This module defines a dataclass `BlackConfig` which stores configuration options
for the Black code formatter, including CLI options and GitHub release resolution.
"""

import sys

from dataclasses import dataclass, field

from commands.git.pre_commit.black.black_validator.black_validator import BlackValidator
from commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher


@dataclass
class BlackConfig:
    
    """
    Configuration holder for the Black Python code formatter.

    Automatically resolves the latest release from GitHub if `rev` is not provided,
    and sets the target Python version based on the current environment.

    Attributes:
        url (str): GitHub repository URL for Black.
        rev (str | None): Git revision or tag. If not set, fetched automatically.
        line_length (int): Maximum line length (default: 88).
        target_version (str | None): Python target version (e.g., 'py311').
        skip_string_normalization (bool): Whether to skip string normalization.
        skip_magic_trailing_comma (bool): Whether to skip magic trailing comma usage.
        check (bool): Whether to enable Black's `--check` mode.
        diff (bool): Whether to show diffs.
        preview (bool): Whether to enable preview mode.
        verbose (bool): Whether to enable verbose output.
        quiet (bool): Whether to suppress output.
        fast (bool): Whether to skip sanity checks for speed.
    """
    
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
        
        """
        Post-initialization logic for setting default values and validating the config.

        If no `rev` is provided, fetches the latest GitHub release tag for Black.
        If no `target_version` is provided, determines the current Python version.
        """
        
        if not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo)
        else:
            BlackValidator.verify_black_version(self.rev)  
            
        if not self.target_version:
            py_version = sys.version_info
            self.target_version = f'py{py_version.major}{py_version.minor}'
            