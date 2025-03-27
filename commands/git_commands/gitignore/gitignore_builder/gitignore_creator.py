import textwrap

from typing import Dict

from SocketIO.commands.git_commands.gitignore.gitignore_definers.gitignore_definers import (
    GitIgnoreVenvDefiner,
    GitIgnoreLogsDefiner,
    GitIgnorePackagingDefiner,
    GitIgnoreOsSpecificFilesDefiner,
    GitIgnoreIDEFilesDefiner,
    GitIgnoreCoverageDefiner,
    GitIgnoreDockerDefiner,
    GitIgnoreGRPCDefiner,
    GitIgnoreJupyterCopyBookDefiner,
    GitIgnoreTestingDefiner,
    GitIgnoreSecurityDefiner,
    GitIgnoreCachesDefiner,
    GitIgnoreByteCodeDefiner
)

class GitIgnoreCreator:
    
    @staticmethod
    def create_file_text (
        options: Dict[str, bool]
    ) -> str:
        
        definers = {
            "bytecode_files": GitIgnoreByteCodeDefiner,
            "venv": GitIgnoreVenvDefiner,
            "logs": GitIgnoreLogsDefiner,
            "packaging": GitIgnorePackagingDefiner,
            "os_specific": GitIgnoreOsSpecificFilesDefiner,
            "ide_files": GitIgnoreIDEFilesDefiner,
            "coverage": GitIgnoreCoverageDefiner,
            "caches": GitIgnoreCachesDefiner,
            "docker": GitIgnoreDockerDefiner,
            "grpc": GitIgnoreGRPCDefiner,
            "jupyter_cp": GitIgnoreJupyterCopyBookDefiner,
            "testing": GitIgnoreTestingDefiner,
            "security": GitIgnoreSecurityDefiner,
        }
        
        sections = [
            definers[key].define(value) for key, value in options.items() if value
        ]
        
        return "\n\n".join(filter(None, sections)).strip()
    
    @staticmethod
    def create(**options: bool) -> None:
        with open('.gitignore', 'w') as f:
            f.write(GitIgnoreCreator.create_file_text(options))
        print(".gitignore has been created.")