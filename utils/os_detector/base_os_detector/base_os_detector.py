"""
Base OS Detector Module

This module defines an abstract base class for detecting the operating system.
It provides a unified interface for OS detection logic used across different components
(e.g., Docker setup, environment configuration, etc.).
"""

from abc import ABC, abstractmethod


class BaseOSDetector(ABC):
    
    """
    Abstract base class for OS detectors.

    Subclasses must implement the `detect` method to return the current operating system name.
    This can be useful in scenarios where conditional behavior is required based on the OS
    (e.g., choosing a package manager, system dependencies, or Docker base images).
    """

    @abstractmethod
    def detect (
        self,
    ) -> str:
        
        """
        Detect and return the name of the current operating system.

        Returns:
            str: The name of the detected operating system (e.g., 'ubuntu', 'macos', 'windows').
        """
        
        pass
