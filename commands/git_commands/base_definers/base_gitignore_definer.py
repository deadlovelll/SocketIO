class BaseGitIgnoreDefiner:
    
    def add_ignorance (
        self,
        ignorance: list[str],
    ) -> str:
        
        return '\n'.join(ignorance)