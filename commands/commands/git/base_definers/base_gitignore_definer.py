"""
Provides a base class for creating the contents of a .gitignore file
by converting a list of ignore patterns into a properly formatted string.
"""

class BaseGitIgnoreDefiner:
    
    """
    Base class for defining .gitignore file content.

    This class provides a utility method to convert a list of ignore patterns
    into the format expected by a .gitignore file.
    """

    def add_ignorance (
        self,
        ignorance: list[str],
    ) -> str:
        
        """
        Converts a list of ignore patterns into a newline-separated string.

        Args:
            ignorance (list[str]): A list of strings representing patterns to ignore.

        Returns:
            str: A newline-separated string of ignore patterns suitable for writing to a .gitignore file.
        """
        
        return '\n'.join(ignorance)
