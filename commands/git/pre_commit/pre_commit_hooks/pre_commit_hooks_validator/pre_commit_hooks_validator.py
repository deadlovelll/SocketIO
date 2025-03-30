import requests

from exceptions.pre_commit_exceptions.pre_commit_exceptions import InvalidPreCommitHooksVersion

class PreCommitHooksValidator:
    
    @staticmethod
    def verify (
        version: str,
    ) -> None:
        
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
        
        url = f"https://api.github.com/repos/pre-commit/pre-commit-hooks/git/refs/tags/{version}"
        try:
            response = requests.get(url, timeout=5)
            return response.json().get('message') != 'Not Found'
        
        except requests.RequestException:
            raise InvalidPreCommitHooksVersion(version)