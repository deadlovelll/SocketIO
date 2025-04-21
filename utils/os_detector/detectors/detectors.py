"""
Operating System Detectors

This module provides concrete implementations of the BaseOSDetector class
for different operating systems such as Windows, macOS, and various Linux distributions.
"""

from utils.os_detector.base_os_detector.base_os_detector import BaseOSDetector


class WindowsDetector(BaseOSDetector):
    
    """
    OS detector for Windows.
    """

    def detect (
        self,
    ) -> str:
        
        """
        Returns:
            str: The name of the OS, which is 'windows'.
        """
        
        return 'windows'


class MacOSDetector(BaseOSDetector):
    
    """
    OS detector for macOS.
    """

    def detect (
        self,
    ) -> str:
        
        """
        Returns:
            str: The name of the OS, which is 'macos'.
        """
        
        return 'macos'


class LinuxDetector(BaseOSDetector):
    
    """
    OS detector for Linux distributions.
    Attempts to identify the specific distro from /etc/os-release.
    """

    def detect (
        self,
    ) -> str:
        
        """
        Detect the Linux distribution name if possible.

        Returns:
            str: The name of the detected Linux distribution or 'linux' if unknown.
        """
        
        distro = self._detect_linux_distro()
        return distro if distro else 'linux'

    def _detect_linux_distro (
        self,
    ) -> str:
        
        """
        Attempts to determine the Linux distribution
        by parsing the /etc/os-release file.

        Returns:
            str: The name of the Linux distro if identified, otherwise an empty string.
        """
        
        try:
            with open('/etc/os-release') as f:
                info = f.read().lower()
                for distro in ('ubuntu', 'debian', 'alpine', 'centos', 'arch'):
                    if distro in info:
                        return distro
        except FileNotFoundError:
            return ''
        return ''


class UnknownOSDetector(BaseOSDetector):
    
    """
    Fallback OS detector if the operating system cannot be identified.
    """

    def detect (
        self,
    ) -> str:
        
        """
        Returns:
            str: A fallback string representing an unknown OS.
        """
        
        return 'unknown'
