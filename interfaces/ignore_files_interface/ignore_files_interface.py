"""
Base class for defining file ignorance logic.

This class serves as a placeholder for the logic to manage files that should be ignored 
during some process (e.g., file processing, migration, or backup). The method `add_ignorance` 
is intended to be implemented by subclasses to define how files are marked as ignored.
"""

from abc import ABC, abstractmethod


class IgnoreFileDefiner:
    
    """
    Class responsible for defining the logic to add ignorance to files.

    This class provides a mechanism for handling files that should be ignored. Subclasses 
    should implement the `add_ignorance` method to define how specific files are marked as 
    "ignored" in the context of file processing, migration, or other relevant processes.

    The class is intended to be extended to support various use cases for file ignorance 
    strategies.

    Methods:
    - `add_ignorance`: Marks a file or files as ignored, based on subclass-specific logic.
    """

    @abstractmethod
    def add_ignorance(self):
        
        """
        Abstract method to define how files are marked as ignored.

        This method should be implemented by subclasses to provide the logic for marking 
        files to be ignored. The specific mechanism depends on the subclass and the 
        context in which the file ignoring is needed.

        Raises:
        - NotImplementedError: If called directly on the base class.
        """
        
        ...
