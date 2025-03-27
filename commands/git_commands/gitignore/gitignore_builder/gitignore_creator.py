from typing import Dict

from commands.git_commands.gitignore.gitignore_definers.gitignore_definers import (
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
            definers[key]().define(value) for key, value in options.items() if value
        ]
        
        return "\n\n".join(filter(None, sections)).strip()
    
    @staticmethod
    def create_file (
        bytecode_files: bool = True,
        venv: bool = True,
        logs: bool = True,
        packaging: bool = True,
        os_specific: bool = True,
        ide_files: bool = True,
        coverage: bool = False,
        caches: bool = True,
        docker: bool = False,
        grpc: bool = False,
        jupyter_cp: bool = False,
        testing: bool = False,
        security: bool = True,
    ) -> None:
        
        options = {
            "bytecode_files": bytecode_files,
            "venv": venv,
            "logs": logs,
            "packaging": packaging,
            "os_specific": os_specific,
            "ide_files": ide_files,
            "coverage": coverage,
            "caches": caches,
            "docker": docker,
            "grpc": grpc,
            "jupyter_cp": jupyter_cp,
            "testing": testing,
            "security": security,
        }

        with open('.gitignore', 'w') as f:
            f.write(GitIgnoreCreator.create_file_text(options))
            
        print(".gitignore has been created.")