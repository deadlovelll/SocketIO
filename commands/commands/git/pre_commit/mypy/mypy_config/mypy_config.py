"""
This module defines a configuration dataclass for setting up Mypy, a static type checker for Python.

The `MypyConfig` class encapsulates all necessary settings required to integrate Mypy 
into a development workflow, particularly in the context of automated pre-commit hooks. 
It supports fetching the latest release tag from the Mypy GitHub repository and includes 
fine-grained options for controlling the type checking behavior.
"""

from dataclasses import dataclass, field
from typing import Optional

from commands.commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher


@dataclass
class MypyConfig:
    
    """
    Configuration settings for Mypy, a static type checker for Python.

    This class holds the configuration options for Mypy, including the repository URL, 
    the version/revision to use, and various Mypy-specific settings such as file locations 
    and typing preferences. The `__post_init__` method fetches the latest release version
    if not explicitly provided.

    Attributes:
        url (str): The URL of the Mypy GitHub repository.
        rev (str): The version/revision of Mypy to use. If not provided, the latest release is fetched.
        config_file (Optional[str]): The name of the Mypy configuration file (default is 'mypy.ini').
        python_version (Optional[str]): The Python version to target (e.g., '3.8').
        ignore_missing_imports (bool): If True, ignores missing imports (default is True).
        disallow_untyped_defs (bool): If True, disallows functions with untyped definitions (default is False).
        strict_optional (bool): If True, enables strict optional checking (default is False).
        check_untyped_defs (bool): If True, checks untyped function definitions (default is True).
        no_implicit_optional (bool): If True, disallows implicit `Optional` types (default is False).
        show_error_codes (bool): If True, shows error codes in output (default is True).
        warn_unused_ignores (bool): If True, warns on unused `# type: ignore` comments (default is True).
        exclude (Optional[str]): A regex pattern to exclude files from Mypy checking.
    """
    
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
        
        """
        Initializes the Mypy configuration by fetching the latest release version if not provided.

        If the `rev` attribute is not specified, the latest release version of Mypy is fetched 
        using the `LastReleaseFetcher` class. Otherwise, the provided version is used.

        If `rev` is explicitly provided, no version fetch is performed.
        """
        
        if  not self.rev:
            owner_repo = self.url.split("https://github.com/")[1]
            self.rev = LastReleaseFetcher.fetch(owner_repo, True)