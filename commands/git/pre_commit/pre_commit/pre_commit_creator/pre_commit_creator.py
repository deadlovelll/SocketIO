from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.black.black_creator.black_creator import BlackCreator
from commands.git.pre_commit.isort.isort_creator.isort_creator import IsortCreator
from commands.git.pre_commit.mypy.mypy_creator.mypy_creator import MypyCreator
from commands.git.pre_commit.pre_commit_config.pre_commit_config import PreCommitConfig
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_creator.pre_commit_hooks_creator import PreCommitHooksCreator

class PreCommitConfigCreator(FileCreator):
    
    PRE_COMMIT_MAP = {
        'precommithooks': PreCommitHooksCreator.create_file,
        'black': BlackCreator.create_file,
        'isort': IsortCreator.create_file,
        'mypy': MypyCreator.create_file,
    }

    @staticmethod
    def create_file(
        **options,
    ) -> None:
        
        config = PreCommitConfig(**options)

        for key, creator_func in PreCommitConfigCreator.PRE_COMMIT_MAP.items():
            if getattr(config, key, False):
                creator_func()