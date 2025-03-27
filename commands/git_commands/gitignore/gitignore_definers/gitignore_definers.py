from commands.git_commands.base_definers.base_gitignore_definer import BaseGitIgnoreDefiner

class GitIgnoreByteCodeDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        bytecode_files: bool,
    ) -> str:
        
        if bytecode_files:
            return super().add_ignorance (
                '__pycache__/',
                '*.py[cod]',
                '*$py.class',
                '*.pyc',
                '*.pyd',
                '*.pyo',
            )
        return ''


class GitIgnoreVenvDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        venv: bool,
    ) -> str:
        
        if venv:
            return super().add_ignorance (
                'venv/',
                'env/',
                '.venv/',
                'ENV/',
            )
        return ''
            
    
class GitIgnoreLogsDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        logs: bool,
    ) -> str:
        
        if logs:
            return super().add_ignorance (
                '*.log',
                '*.sqlite3',
                '*.db',
                '*.sql',
            )
        return ''
    
    
class GitIgnorePackagingDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        packaging: bool,
    ) -> str:
        
        if packaging:
            return super().add_ignorance (
                'build/',
                'dist/',
                '*.egg-info/',
                'pip-wheel-metadata/',
            )
        return ''
    
    
class GitIgnoreOsSpecificFilesDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        os_specific: bool,
    ) -> str:
        
        if os_specific:
            return super().add_ignorance (
                '.DS_Store',
                'Thumbs.db',
            )
        return ''
    
    
class GitIgnoreIDEFilesDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        ide_files: bool,
    ) -> str:
        
        if ide_files:
            return super().add_ignorance (
                '.idea/',
                '.vscode/',
                '*.swp',
                '*.swo',
                '*.swn',
            )
        return ''
    
    
class GitIgnoreCoverageDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        coverage: bool,
    ) -> str:
        
        if coverage:
            return super().add_ignorance (
                '.coverage',
                'htmlcov/',
                'coverage.xml',
            )
        return ''
            
            
class GitIgnoreCachesDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        caches: bool,
    ) -> str:
        
        if caches:
            return super().add_ignorance (
                '.cache/',
                '*.mypy_cache/',
                '.pytest_cache/',
            )
        return ''
    
    
class GitIgnoreDockerDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        docker: bool,
    ) -> str:
        
        if docker:
            return super().add_ignorance (
                'docker-compose.override.yml',
                '*.dockerfile',
                '*.tar',
            )
        return ''
    
    
class GitIgnoreGRPCDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        grpc: bool,
    ) -> str:
        
        if grpc:
            return super().add_ignorance (
                '*_pb2.py',
                '*_pb2_grpc.py',
            )
        return ''
    
    
class GitIgnoreJupyterCopyBookDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        jupyter_cp: bool,
    ) -> str:
        
        if jupyter_cp:
            return super().add_ignorance (
                '.ipynb_checkpoints/',
            )
        return ''
    

class GitIgnoreTestingDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        testing: bool,
    ) -> str:
        
        if testing:
            return super().add_ignorance (
                'test-reports/',
                'tests/__pycache__/',
            )
    
    
class GitIgnoreSecurityDefiner(BaseGitIgnoreDefiner):
    
    def define (
        self,
        security: bool,
    ) -> str:
        
        if security:
            return super().add_ignorance (
                '.env',
                '.env.*',
                'config.yaml',
                'secrets.json',
                'secrets.env',
            )