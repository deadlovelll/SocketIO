"""
This module provides a validation utility for verifying the existence
of specific versions (tags) of the `pre-commit-hooks` repository on GitHub.
"""

import requests

from exceptions.pre_commit_exceptions.pre_commit_exceptions import InvalidPreCommitHooksVersion


class PreCommitHooksValidator:
    
    """
    Provides static methods to validate versions of `pre-commit-hooks` from GitHub.
    """
    
    @staticmethod
    def verify (
        version: str,
    ) -> None:
        
        """
        Verifies the validity of the specified version using all registered validators.

        Args:
            version (str): The version tag to verify.

        Raises:
            InvalidPreCommitHooksVersion: If the version is not found on GitHub.
        """
        
        validators = {
            'verify_pre_commit_hooks_version': version,
        }
        
        for method, args in validators.items():
            func = getattr(PreCommitHooksValidator, method)
            func(*args if isinstance(args, tuple) else (args,))
    
    @staticmethod
    def verify_pre_commit_hooks_version (
        version: str,
    ) -> bool:
        
        """
        Checks if a given version of `pre-commit-hooks` exists on GitHub.

        Args:
            version (str): The tag name to verify.

        Returns:
            bool: True if the tag exists, False otherwise.

        Raises:
            InvalidPreCommitHooksVersion: If the request fails or the tag is not found.
        """
        
        url = f"https://api.github.com/repos/pre-commit/pre-commit-hooks/git/refs/tags/{version}"
        try:
            response = requests.get(url, timeout=5)
            return response.json().get('message') != 'Not Found'
        
        except requests.RequestException:
            raise InvalidPreCommitHooksVersion(version)