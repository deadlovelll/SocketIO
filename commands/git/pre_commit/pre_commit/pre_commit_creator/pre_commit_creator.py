from typing import override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.black.black_creator.black_creator import BlackCreator
from commands.git.pre_commit.isort.isort_creator.isort_creator import IsortCreator
from commands.git.pre_commit.mypy.mypy_creator.mypy_creator import MypyCreator
from commands.git.pre_commit.pre_commit.pre_commit_config.pre_commit_config import PreCommitConfig
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_creator.pre_commit_hooks_creator import PreCommitHooksCreator

from commands.base_command.base_command import BaseCommand

class PreCommitConfigCreator (
    BaseCommand, 
    FileCreator,
):
    
    def __init__ (
        self,
        **options,
    ) -> None:
        
        super().__init__(**options)
    
        self.PRE_COMMIT_MAP = {
            'precommithooks': PreCommitHooksCreator,
            'black': BlackCreator,
            'isort': IsortCreator,
            'mypy': MypyCreator,
        }

    def create_file (
        self,
    ) -> None:
        
        config = PreCommitConfig(**self.options)

        for key, creator in self.PRE_COMMIT_MAP.items():
            if getattr(config, key, False):
                creator(**self.options).execute()
    
    @override            
    def execute (
        self,
    ) -> None:
        
        self.create_file()