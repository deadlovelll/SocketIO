from interfaces.file_creator_interface.file_creator_interface import FileCreator

class PreCommitConfigCreator(FileCreator):
    
    def create_file_text (
        self,
    ) -> str:
        
        pass
    
    def create_file (
        self,
        precommit_hooks: bool,
        black: bool,
        isort: bool,
        custom_linter: bool,
    ) -> None:
        
        pass