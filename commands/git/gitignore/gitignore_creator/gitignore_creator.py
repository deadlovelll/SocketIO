from typing import Dict, Optional, override, Type

from commands.git.gitignore.gitignore_definers.gitignore_definers import (
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

from commands.base_command.base_command import BaseCommand

class GitIgnoreCreator(BaseCommand):
    
    def __init__ (
        self, 
        **options,
    ) -> None:
        
        super().__init__(**options)
        
        self.definers: Dict[str, Type] = {
            'bytecode_files': GitIgnoreByteCodeDefiner,
            'venv': GitIgnoreVenvDefiner,
            'logs': GitIgnoreLogsDefiner,
            'packaging': GitIgnorePackagingDefiner,
            'os_specific': GitIgnoreOsSpecificFilesDefiner,
            'ide_files': GitIgnoreIDEFilesDefiner,
            'coverage': GitIgnoreCoverageDefiner,
            'caches': GitIgnoreCachesDefiner,
            'docker': GitIgnoreDockerDefiner,
            'grpc': GitIgnoreGRPCDefiner,
            'jupyter_cp': GitIgnoreJupyterCopyBookDefiner,
            'testing': GitIgnoreTestingDefiner,
            'security': GitIgnoreSecurityDefiner,
        }
    
    def create_file_text (
        self,
    ) -> str:
        
        sections = []

        for key, value in self.options.items():
            definer_cls = self.definers.get(key)
            if definer_cls and value:
                section = definer_cls().define(value)
                if section:
                    sections.append(section)

        return '\n\n'.join(sections).strip()
    
    def create_file (
        self,
    ) -> None:
        
        content = self.create_file_text()

        with open('.gitignore', 'w') as f:
            f.write(content)
            
        print('.gitignore has been created.')
        
    @override
    def execute (
        self,
    ) -> None:
        
        self.create_file()