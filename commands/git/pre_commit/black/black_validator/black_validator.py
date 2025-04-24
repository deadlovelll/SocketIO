"""
Module for validating Black formatter versions via GitHub API.

Provides utilities for verifying whether a specific version tag
of the `psf/black` repository exists.
"""

import requests
from exceptions.black_exceptions.black_exceptions import InvalidBlackVersion


class BlackValidator:
    
    """
    Validator class for checking the existence of Black formatter versions on GitHub.

    Uses GitHub's REST API to check whether a specified version tag is valid.
    """

    @staticmethod
    def verify (
        version: str,
    ) -> None:
        
        """
        Entry point to trigger all version-related validations.

        Currently, delegates to `verify_black_version`.

        Args:
            version (str): The version string to validate (e.g., '22.3.0').

        Raises:
            InvalidBlackVersion: If the version is not valid or the check fails.
        """
        
        validators = {
            'verify_black_version': version,
        }
        
        for method, args in validators.items():
            func = getattr(BlackValidator, method)
            func(*args if isinstance(args, tuple) else (args,))
    
    @staticmethod
    def verify_black_version (
        version: str,
    ) -> bool:
        
        """
        Validates whether a given version tag exists on GitHub for `psf/black`.

        Args:
            version (str): The version string to check (e.g., '22.3.0').

        Returns:
            bool: True if the version exists, False otherwise.

        Raises:
            InvalidBlackVersion: If the GitHub request fails or the tag is not found.
        """
        
        url = f"https://api.github.com/repos/psf/black/git/refs/tags/{version}"
        try:
            response = requests.get(url, timeout=5)
            return response.json().get('message') != 'Not Found'
        
        except requests.RequestException:
            raise InvalidBlackVersion(version)