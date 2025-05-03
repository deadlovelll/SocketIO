"""
Configuration module for the isort pre-commit hook.

This module defines a dataclass `IsortConfig` that encapsulates configuration
options for the `isort` code formatter, including its GitHub release URL, versioning,
formatting preferences, and compatibility with `black` and other profiles.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from commands.commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher


@dataclass
class IsortConfig:
    
    """
    Configuration model for the isort tool used in pre-commit hooks.

    Attributes:
        url (str): The GitHub URL for the isort repository (non-init field).
        rev (str): The version tag or commit hash for isort to use. If None, fetched automatically.
        profile (str): Code style profile. Default is 'black'.
        check_only (bool): Whether to run in check-only mode (no changes applied). Defaults to True.
        diff (bool): Whether to show diffs on changes. Defaults to True.
        line_length (int): Max line length before breaking imports. Defaults to 88.
        skip (List[str]): List of file paths or patterns to skip during formatting.
        virtual_env (Optional[str]): Path to the virtual environment (for import context).
        src (List[str]): List of source folders to apply `isort` to.
        float_to_top (bool): Whether to move all imports to the top of the file. Defaults to False.
        profiles (List[str]): Available profiles for formatting (class-level constant).
    """
    
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
        
        """
        Automatically fetches the latest release version of isort from GitHub if not provided.

        Uses `LastReleaseFetcher` to fetch the latest tag from the PyCQA/isort repository.
        """
        
        if not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo)