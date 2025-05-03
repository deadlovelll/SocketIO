"""
This module provides functionality for retrieving the latest release or tag version
of a public GitHub repository using the GitHub REST API.
"""

import requests


class LastReleaseFetcher:
    
    @staticmethod
    def fetch (
        repo_name: str,
        tags: bool = False,
    ) -> str:
        
        """
        Fetches the latest release or tag for a given repository.

        Args:
            repo_name (str): The name of the GitHub repository (in the format 'owner/repo').
            tags (bool, optional): Whether to fetch the latest tag. Defaults to False (fetches latest release).

        Returns:
            str: The version information (either release or tag) or None if the fetch fails.
        """
        
        if not tags:
            return LastReleaseFetcher.fetch_default(repo_name)
        else:
            return LastReleaseFetcher.fetch_tag(repo_name)
    
    @staticmethod
    def fetch_default (
        repo_name: str,
    ) -> str:
        
        """
        Fetches the latest release version for a given repository.

        Args:
            repo_name (str): The name of the GitHub repository (in the format 'owner/repo').

        Returns:
            str: The latest release version, or None if the fetch fails.
        """
        
        url = 'https://api.github.com/repos/' + repo_name + '/releases/latest'
        return LastReleaseFetcher.get_verison(url)
    
    @staticmethod
    def fetch_tag (
        repo_name: str,
    ) -> str:
        
        """
        Fetches the latest tag for a given repository.

        Args:
            repo_name (str): The name of the GitHub repository (in the format 'owner/repo').

        Returns:
            str: The latest tag, or None if the fetch fails.
        """
        
        url = 'https://api.github.com/repos/' + repo_name + '/tags'
        return LastReleaseFetcher.get_verison(url)
        
    @staticmethod 
    def get_verison (
        url: str,
    ) -> str:
        
        """
        Makes an API request to GitHub to fetch version data.

        Args:
            url (str): The URL to request data from GitHub's API.

        Returns:
            str: The version (either release or tag), or None if there was an error fetching the data.
        """        

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('tag_name') if isinstance(data, dict) else data[0]['name']
        
        except (requests.RequestException, KeyError):
            print('Warning: Failed to fetch required version.')
            return None