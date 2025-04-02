import requests

class BlackValidator:

    @staticmethod
    def verify (
        version: str,
    ) -> None:
        
        validators = {
            'verify_pre_commit_hooks_version': version,
        }
        
        for method, args in validators.items():
            func = getattr(BlackValidator, method)
            func(*args if isinstance(args, tuple) else (args,))
    
    @staticmethod
    def verify_pre_commit_hooks_version (
        version: str,
    ) -> bool:
        
        url = f"https://api.github.com/repos/psf/black/git/refs/tags/{version}"
        try:
            response = requests.get(url, timeout=5)
            return response.json().get('message') != 'Not Found'
        
        except requests.RequestException:
            raise InvalidPreCommitHooksVersion(version)