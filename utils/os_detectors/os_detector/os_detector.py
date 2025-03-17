import platform

from os_detectors.base_os_detector.base_os_detector import BaseOSDetector
from os_detectors.detectors.detectors import (
    WindowsDetector,
    MacOSDetector,
    LinuxDetector,
    UnknownOSDetector,
)

class OSDetector:
    
    """
    The OSDetector class encapsulates the logic to choose the appropriate
    OS detector based on the current platform.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        self.system = platform.system().lower()
        self.detector = self._select_detector()
        
        self.os_map = {
            'windows': WindowsDetector,
            'darwin': MacOSDetector,
            'linux': LinuxDetector,
        }

    def _select_detector (
        self,
    ) -> BaseOSDetector:
        
        """
        Chooses the appropriate OS detector class based on the system type.
        """
        
        try:
            return self.os_map[self.system]()
        except Exception:
            return UnknownOSDetector()

    def detect (
        self,
    ) -> str:
        
        """
        Delegates the detection to the selected OS detector.
        """
        
        return self.detector.detect()