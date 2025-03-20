from commands.docker_commands.docker_definers.base_definer.base_definer import BaseDockerDefiner
from commands.docker_commands.docker_definers.base_definer.base_dockerignore_definer import BaseDockerignoreDefiner

class PythonCacheDefiner(BaseDockerDefiner, BaseDockerignoreDefiner):
    
    @classmethod
    def define (
        cls,
        python_cache: bool,
    ) -> str:
        
        if python_cache:
            return super().add_ignorance (
                [
                    '__pycache__/',
                    '*.pyc',
                    '*.pyo',
                    '*.pyd',
                ]
            )
        return ''

class VenvDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        virtual_environment: bool,
    ) -> str:
        
        if virtual_environment:
            return super().add_ignorance (
                [
                    'venv/',
                    '.env/',
                    '.venv/',
                ]
            )
        return ''
    
class SystemSpecsDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        system_spec_files: bool,
    ) -> str:
        
        if system_spec_files:
            return super().add_ignorance (
                [
                    '.DS_Store',
                    'Thumbs.db',
                    '.idea/',
                    '.vscode/',
                    '*.iml',
                ]
            )
        return ''
    
class LogsDefine(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        logs: bool,
    ) -> str:
        
        if logs:
            return super().add_ignorance (
                [
                    'logs/',
                    '*.log',
                    '*.out',
                    '*.err',
                    'tmp/',
                    '*.swp',
                    '*.swo',
                    'coverage/',
                    '*.cover',
                    '.pytest_cache/',
                ]
            )
            
class TestCoverageDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        test_coverage: bool,
    ) -> str:
        
        if test_coverage:
            return super().add_ignorance (
                [
                    'tests/',
                    'coverage/',
                    '*.cover',
                    '*.pytest_cache/',
                ]
            )
        return ''
    

class GitAttributesDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        git: bool,
    ) -> str:
        
        if git:
            return super().add_ignorance (
                [
                    '.git/',
                    '.gitignore',
                    '.idea/',
                    '.vscode/',
                    '*.iml',
                ]
            )
        return ''
    
    
class DockerFilesDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        docker: bool,
    ) -> str:
        
        if docker:
            return super().add_ignorance (
                [
                    '.dockerignore',
                    'Dockerfile*',
                    'docker-compose.yml',
                ]
            )
        return ''

class PoetryDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        poetry: bool,
    ) -> str:
        
        if poetry:
            return super().add_ignorance (
                [
                    '.poetry/'
                ]
            )
        return ''

class CompiledFiledDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        compiled_files: bool,
    ) -> str:
        
        if compiled_files:
            return super().add_ignorance (
                [
                    'dist/',
                    'build/',
                    '*.egg-info/',
                ]
            )
        return ''


class DocumentationDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        documentation: bool,
    ) -> str:
        
        if documentation:
            return super().add_ignorance (
                [
                    'docs/',
                    '*.md',
                    '*.rst',
                ]
            )
        return ''
    

class EnvFilesDefiner(BaseDockerignoreDefiner, BaseDockerDefiner):
    
    @classmethod
    def define (
        cls,
        env_files: bool,
    ) -> str:
        
        if env_files:
            return super().add_ignorance (
                [
                    '*.env',
                ]
            )
        return ''
