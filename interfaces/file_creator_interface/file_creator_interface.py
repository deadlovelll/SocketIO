"""
Base class for file creation operations.

This module defines the abstract base class `FileCreator` which provides an interface for 
creating files with specific content and file creation logic. The purpose of this class is 
to be inherited by concrete classes that implement the actual logic for creating files 
and generating their contents.

Subclasses must implement the `create_file_text()` and `create_file()` methods to define 
how the file's content is generated and how the file itself is created.
"""

from abc import ABC, abstractstaticmethod


class FileCreator(ABC):
    
    """
    Abstract base class for creating files.

    This class defines the blueprint for creating files with specific content. Any class 
    inheriting from `FileCreator` must implement the `create_file_text()` method to generate 
    the content and the `create_file()` method to create the file using the generated content.

    The primary purpose of this class is to serve as an interface for various file creation 
    strategies that may differ based on file type, format, or storage medium.

    Subclasses must implement the abstract methods:
    - `create_file_text`: Defines the content to be written to the file.
    - `create_file`: Handles the actual file creation process using the generated content.
    """

    @abstractstaticmethod
    def create_file_text(
        self,
    ) -> str:
        
        """
        Abstract method to generate the file content.

        This method should return the content that needs to be written to the file. 
        The content can be generated dynamically, fetched from other sources, or 
        generated using class-specific logic.

        Returns:
        - str: The content to be written to the file.

        Raises:
        - NotImplementedError: If called directly on the base class.
        """
        
        ...
    
    @abstractstaticmethod
    def create_file(
        self,
    ) -> None:
        
        """
        Abstract method to create the file.

        This method is responsible for creating the file using the content generated 
        by the `create_file_text()` method. Subclasses should implement this method 
        to handle file creation, whether it's writing to disk, cloud storage, or other 
        destinations.

        Raises:
        - NotImplementedError: If called directly on the base class.
        """
        
        ...
