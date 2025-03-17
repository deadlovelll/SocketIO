from os_detectors.base_os_detector.base_os_detector import BaseOSDetector

class WindowsDetector(BaseOSDetector):
    
    def detect (
        self,
    ) -> str:
        
        return 'windows'


class MacOSDetector(BaseOSDetector):
    
    def detect (
        self,
    ) -> str:
        
        return 'macos'


class LinuxDetector(BaseOSDetector):
    
    def detect (
        self,
    ) -> str:
        
        distro = self._detect_linux_distro()
        return distro if distro else 'linux'
    
    def _detect_linux_distro (
        self,
    ) -> str:
        
        """Attempts to determine the Linux 
        distribution by reading /etc/os-release."""
        
        try:
            with open('/etc/os-release') as f:
                info = f.read().lower()
                for distro in (
                    'ubuntu', 
                    'debian', 
                    'alpine', 
                    'centos', 
                    'arch',
                ):
                    if distro in info:
                        return distro
        except FileNotFoundError:
            return ''
        return ''
        
class UnknownOSDetector(BaseOSDetector):
    
    def detect (
        self,
    ) -> str:
        
        return 'unknown'