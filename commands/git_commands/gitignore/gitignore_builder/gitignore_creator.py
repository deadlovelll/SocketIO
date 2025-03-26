import textwrap

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
    
    @staticmethod
    def create_file_text (
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
    ) -> str:
        
        sections = [
            GitIgnoreVenvDefiner.define(venv),
            GitIgnoreLogsDefiner.define(logs),
            GitIgnorePackagingDefiner.define(packaging),
            GitIgnoreOsSpecificFilesDefiner.define(os_specific),
            GitIgnoreIDEFilesDefiner.define(ide_files),
            GitIgnoreCoverageDefiner.define(coverage),
            GitIgnoreDockerDefiner.define(docker),
            GitIgnoreGRPCDefiner.define(grpc),
            GitIgnoreJupyterCopyBookDefiner.define(jupyter_cp),
            GitIgnoreTestingDefiner.define(testing),
            GitIgnoreSecurityDefiner.define(security),
        ]
        
        content = "\n\n".join(filter(None, sections))

        return textwrap.dedent(content).strip()
    
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
    ) -> None:
        
        with open('.dockerignore', 'w') as f:
            f.write(GitIgnoreCreator.create_file_text (
                bc,
                venv,
                logs,
                packaging,
                os_specific,
                ide_files,
                coverage,
                docker,
                grpc,
                jupyter_cp,
                testing,
                security,
            ))
        print(f".gitignore has been created.")