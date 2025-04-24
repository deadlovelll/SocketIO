"""
Defines the configuration flags for enabling or disabling individual pre-commit hooks
such as Black, Isort, Mypy, and optionally a custom linter.
"""

from dataclasses import dataclass


@dataclass
class PreCommitConfig:
    
    """
    Represents a high-level configuration for enabling/disabling individual pre-commit hooks.

    Attributes:
        precommithooks (bool): Whether pre-commit hooks are enabled at all.
        black (bool): Enables or disables the Black formatter hook.
        isort (bool): Enables or disables the Isort import sorter hook.
        mypy (bool): Enables or disables the Mypy static type checker hook.
        custom_linter (bool): Enables or disables a custom linter hook.
    """
    
    precommithooks: bool = True
    black: bool = True
    isort: bool = True
    mypy: bool = True
    custom_linter: bool = False