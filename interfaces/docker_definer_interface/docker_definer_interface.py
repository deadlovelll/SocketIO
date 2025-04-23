"""
Base class for defining Docker configurations.

This module defines the abstract base class `BaseDockerDefiner` for creating specific Docker 
configuration definers. The purpose of this class is to establish a blueprint for Docker 
configuration classes that need to implement the `define()` method.

Each subclass must implement the `define()` method to provide the specific Docker configuration 
logic required for the application.
"""

from abc import ABC, abstractstaticmethod

class BaseDockerDefiner(ABC):
    
    """
    Abstract base class for defining Docker configurations.

    This class serves as a base for creating classes that define Docker container 
    configurations. It establishes a common interface that any Docker configuration class 
    must implement by overriding the `define()` method.

    Subclasses of `BaseDockerDefiner` must provide their own implementation of the `define()` 
    method to specify the actual Docker configuration logic.
    """

    @abstractstaticmethod
    def define():
        
        """
        Abstract method to define Docker configuration.

        This method must be implemented by any subclass to define the necessary Docker 
        configurations for a container.

        The implementation should include details such as environment variables, ports, 
        volumes, and any other configurations relevant to the container.
        """
        
        pass
