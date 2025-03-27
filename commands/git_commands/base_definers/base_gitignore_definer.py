class BaseGitIgnoreDefiner:
    
    def add_ignorance (
        ignorance: list[str],
    ) -> str:
        
        return '\n'.join(ignorance)