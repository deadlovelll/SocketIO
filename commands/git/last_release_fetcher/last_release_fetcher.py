import requests

class LastReleaseFetcher:
    
    @staticmethod
    def fetch (
        repo_name,
        tags: bool = False,
    ) -> str:
        
        if not tags:
            LastReleaseFetcher.fetch_default(repo_name)
        else:
            LastReleaseFetcher.fetch_tag(repo_name)
    
    @staticmethod
    def fetch_default(repo_name):
        url = 'https://api.github.com/repos/' + repo_name + '/releases/latest'
        return LastReleaseFetcher.get_verison(url)
    
    @staticmethod
    def fetch_tag(repo_name):
        url = 'https://api.github.com/repos/' + repo_name + '/tags'
        print(url)
        return LastReleaseFetcher.get_verison(url)
        
    @staticmethod 
    def get_verison(url):
        try:
            response = requests.get(url, timeout=5)
            print(response)
            response.raise_for_status()
            data = response.json()
            return data.get('tag_name') if isinstance(data, dict) else data[0]['name']
        
        except (requests.RequestException, KeyError):
            print('Warning: Failed to fetch required version.')
            return None