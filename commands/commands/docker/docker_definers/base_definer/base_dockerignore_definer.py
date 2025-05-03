"""
BaseDockerignoreDefiner module.

Provides a base utility class for generating `.dockerignore` content from a list
of patterns that should be ignored in the Docker build context.
"""


class BaseDockerignoreDefiner:
    
    """
    Base class for Dockerignore definers.

    Provides utility method to convert a list of ignore patterns into `.dockerignore`-formatted text.
    """

    @staticmethod
    def add_ignorance(
        ignorance: list[str],
    ) -> str:
        
        """
        Converts a list of ignore patterns into a `.dockerignore` block.

        Args:
            ignorance (list[str]): A list of file or directory patterns to ignore.

        Returns:
            str: Formatted string representing `.dockerignore` content.
        """
        
        return '\n'.join(ignorance)
