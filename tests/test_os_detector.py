import unittest 
from unittest.mock import patch, mock_open

from utils.os_detector.os_detector.os_detector import OSDetector

class TestOsDetector(unittest.TestCase):
    
    @patch (
        'platform.system', 
        return_value='windows',
    )
    def test_windows_detector (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'windows')
    
    @patch (
        'platform.system', 
        return_value='darwin',
    )
    def test_macos_detector (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'macos')
    
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Ubuntu\nVERSION=20.04'),
    )
    @patch (
        'platform.system', 
        return_value='Linux',
    )
    def test_linux_detector_ubuntu (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'ubuntu')
    
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Debian\nVERSION=20.04'),
    )
    @patch (
        'platform.system', 
        return_value='Linux',
    )
    def test_linux_detector_debian (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'debian')
    
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Alpine\nVERSION=20.04'),
    )
    @patch (
        'platform.system', 
        return_value='Linux',
    )
    def test_linux_detector_alpine (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'alpine')
    
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Centos\nVERSION=20.04'),
    )
    @patch (
        'platform.system', 
        return_value='Linux',
    )
    def test_linux_detector_centos (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'centos')
    
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=Arch\nVERSION=20.04'),
    )
    @patch (
        'platform.system', 
        return_value='Linux',
    )
    def test_linux_detector_arch (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'arch')
    
    @patch (
        'builtins.open', 
        mock_open(read_data='NAME=unknown\nVERSION=20.04'),
    )
    @patch (
        'platform.system', 
        return_value='Linux',
    )
    def test_linux_detector_unknown (
        self,
        mock_system,
    ) -> None:
        
        os_detector = OSDetector()
        os = os_detector.detect()
        self.assertEqual(os, 'linux')