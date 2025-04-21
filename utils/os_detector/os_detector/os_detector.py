"""
OS Detector Module

Provides a unified interface to detect the current operating system.
Maps system identifiers to specific detector classes.
"""

import platform

from utils.static.privacy.privacy import privatemethod
from utils.static.privacy.protected_class import ProtectedClass
from utils.os_detector.base_os_detector.base_os_detector import BaseOSDetector
from utils.os_detector.detectors.detectors import (
    WindowsDetector,
    MacOSDetector,
    LinuxDetector,
    UnknownOSDetector,
)


class OSDetector(ProtectedClass):
    
    """
    OSDetector encapsulates the logic to select the appropriate OS detector
    class based on the current platform.

    It provides a unified `detect()` method that returns the name of the
    current operating system or distribution.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the OSDetector by selecting the appropriate OS detection strategy
        based on the current platform.system().
        """
        
        self._os_map = {
            'windows': WindowsDetector,
            'darwin': MacOSDetector,
            'linux': LinuxDetector,
        }

        self._system = platform.system().lower()
        self._detector: BaseOSDetector = self._select_detector()

    @privatemethod
    def _select_detector (
        self,
    ) -> BaseOSDetector:
        
        """
        Internal method to select an appropriate detector class
        for the current OS.

        Returns:
            BaseOSDetector: An instance of the appropriate OS detector.
        """
        
        try:
            return self._os_map[self._system]()
        except KeyError:
            return UnknownOSDetector()

    def detect (
        self,
    ) -> str:
        
        """
        Detects the name of the current operating system.

        Returns:
            str: A string representing the detected OS or distribution.
        """
        
        return self._detector.detect()
