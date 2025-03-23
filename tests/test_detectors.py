import unittest
from unittest.mock import mock_open, patch

from utils.os_detector.detectors.detectors import (
    WindowsDetector,
    LinuxDetector,
    MacOSDetector,
    UnknownOSDetector,
)

class TestDetectors(unittest.TestCase):
    
    def test_windows_detector (
        self,
    ) -> None:
        
        windows_detector = WindowsDetector()
        os = windows_detector.detect()
        
        self.assertEqual(os, 'windows')
        
    def test_macos_detector (
        self,
    ) -> None:
        
        macos_detector = MacOSDetector()
        os = macos_detector.detect()
        
        self.assertEqual(os, 'macos')
        
    def test_unknown_os_detector (
        self,
    ) -> None:
        
        unknown_os_detector = UnknownOSDetector()
        os = unknown_os_detector.detect()
        
        self.assertEqual(os, 'unknown')
        
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Ubuntu\nVERSION=20.04'),
    )
    def test_linux_detector_ubuntu (
        self,
    ) -> None:
        
        linux_os_detector = LinuxDetector()
        os = linux_os_detector.detect()
        
        self.assertEqual(os, 'ubuntu')
        
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Debian\nVERSION=20.04'),
    )
    def test_linux_detector_debian (
        self,
    ) -> None:
        
        linux_os_detector = LinuxDetector()
        os = linux_os_detector.detect()
        
        self.assertEqual(os, 'debian')
        
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Alpine\nVERSION=20.04'),
    )
    def test_linux_detector_alpine (
        self,
    ) -> None:
        
        linux_os_detector = LinuxDetector()
        os = linux_os_detector.detect()
        
        self.assertEqual(os, 'alpine')
        
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Centos\nVERSION=20.04'),
    )
    def test_linux_detector_centos (
        self,
    ) -> None:
        
        linux_os_detector = LinuxDetector()
        os = linux_os_detector.detect()
        
        self.assertEqual(os, 'centos')
        
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Arch\nVERSION=20.04'),
    )
    def test_linux_detector_arch (
        self,
    ) -> None:
        
        linux_os_detector = LinuxDetector()
        os = linux_os_detector.detect()
        
        self.assertEqual(os, 'arch')
        
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=unknown\nVERSION=20.04'),
    )
    def test_linux_detector_unknown (
        self,
    ) -> None:
        
        linux_os_detector = LinuxDetector()
        os = linux_os_detector.detect()
        
        self.assertEqual(os, 'linux')