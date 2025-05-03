"""
This module provides validation utilities for isort configurations.
"""

import os
import requests

from exceptions.isort_exceptions.isort_exceptions import InvalidIsortVersion, InvalidIsortProfile

class IsortValidator:
    
    """
    Provides static validation methods for isort configuration fields.

    Includes validation of isort version, profile name, and optionally
    the presence of skipped files or directories.
    """

    @staticmethod
    def verify (
        version: str,
        profile: str,
    ) -> None:
        
        """
        Run all required verifications for version and profile.

        Args:
            version (str): The isort version tag to verify.
            profile (str): The formatting profile to verify.

        Raises:
            InvalidIsortVersion: If the version is invalid.
            InvalidIsortProfile: If the profile is not recognized.
        """
        
        validators = {
            'verify_isort_version': version,
            'verify_isort_profile': profile,
        }
        
        for method, args in validators.items():
            func = getattr(IsortValidator, method)
            func(*args if isinstance(args, tuple) else (args,))
    
    @staticmethod
    def verify_isort_version (
        version: str,
    ) -> None:
        
        """
        Validates whether the provided isort version tag exists on GitHub.

        Args:
            version (str): The version string to validate.

        Raises:
            InvalidIsortVersion: If the version tag does not exist.
        """
        
        url = f"https://api.github.com/repos/PyCQA/isort/git/refs/tags/{version}"
        try:
            response = requests.get(url, timeout=5)
            if response.json().get('message') != 'Not Found':
                raise InvalidIsortVersion(version)
            
            return None
        
        except requests.RequestException:
            raise InvalidIsortVersion(version)

    @staticmethod
    def verify_isort_profile (
        profile: str,
    ) -> None:
        
        """
        Validates whether the given profile name is supported by isort.

        Args:
            profile (str): The profile name to check.

        Raises:
            InvalidIsortProfile: If the profile is not in the allowed list.
        """
        
        profiles = [
            'black'
            'google'
            'pycharm'	
            'attrs'	
            'pep8'
        ]
        
        if profile not in profiles:
            raise InvalidIsortProfile(profile)