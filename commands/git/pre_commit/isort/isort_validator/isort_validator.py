import requests

from exceptions.isort_exceptions.isort_exceptions import InvalidIsortVersion, InvalidIsortProfile

class IsortValidator:

    @staticmethod
    def verify (
        version: str,
        profile: str,
    ) -> None:
        
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
        
        profiles = [
            'black'
            'google'
            'pycharm'	
            'attrs'	
            'pep8'
        ]
        
        if profile not in profiles:
            raise InvalidIsortProfile(profile)
        
    @staticmethod
    def verify_isort_skip (
        skip: list[str],
    ) -> None:
        
        import os
        print(os.getcwd())