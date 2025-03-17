import platform

from utils.os_detector.os_detector.os_detector import OSDetector

class SystemDependenciesDefiner:
    
    @staticmethod
    def define_system_deps (
        install_system_deps: bool, 
        os_type: str,
    ) -> str:
        
        if not install_system_deps:
            return ""
        
        if not os_type:
            os_type = OSDetector().detect()
            print(os_type)
        
        depends_map = SystemDependenciesDefiner._get_os_map()
        
        return depends_map[os_type]
        
    @staticmethod
    def _get_os_map() -> dict:
        
        depends_map = {
            'ubuntu': """\
                RUN apt-get update && \\
                    apt-get install -y --no-install-recommends \\
                    build-essential && \\
                    rm -rf /var/lib/apt/lists/*
                """,
            'alpine': """\
                RUN apk add --no-cache \\
                    build-base
                """,
            'centos': """\
                RUN yum groupinstall -y "Development Tools" && \\
                    yum clean all
                """,
            'arch': """\
                RUN pacman -Syu --noconfirm base-devel
                """,
            'macos': """\
                RUN brew install coreutils
                """,
            'windows': """\
                RUN choco install make mingw
                """,
        }
        
        depends_map['debian'] = depends_map['ubuntu']
        depends_map['rhel'] = depends_map['centos']
        
        return depends_map