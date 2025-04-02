import requests

class LastReleaseFetcher:
    
    @staticmethod
    def fetch (
        repo_name,
    ) -> str:
        
        api_url = 'https://api.github.com/repos' + repo_name + '/releases/latest'
        
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            return response.json().get('tag_name')
        
        except (requests.RequestException, KeyError):
            print('Warning: Failed to fetch required version.')
            return None