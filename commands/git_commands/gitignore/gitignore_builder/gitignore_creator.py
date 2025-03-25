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
    GitIgnoreSecurityDefiner
)

class GitIgnoreCreator:
    
    def create_file_text():
        pass
    
    def create (
        bc: bool,
        venv: bool,
        logs: bool,
        packaging: bool,
        os_specific: bool,
        ide_files: bool,
        coverage: bool,
        docker: bool,
        grpc: bool,
        jupyter_cp: bool,
        testing: bool,
        security: bool,
    ):
        pass