from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git_commands.pre_commit.pre_commit_hooks.pre_commit_hooks_config.pre_commit_hooks_config import PreCommitHooksConfig

class PreCommitHooksBuilder(FileCreator):
    
    @staticmethod
    def create_file_text():
        pass
    
    @staticmethod
    def create_file(**options):
        
        config = PreCommitHooksConfig(**options)