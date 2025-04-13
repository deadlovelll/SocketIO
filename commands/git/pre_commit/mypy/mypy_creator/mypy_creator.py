import yaml

from pathlib import Path
from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.mypy.mypy_config.mypy_config import MypyConfig
from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator

class MypyCreator(BaseHookCreator, FileCreator):
    
    def __init__ (
        self, 
        **options,
    ) -> None:
        
        super().__init__(**options)
        
    @override
    def generate_args (
        self,
        config: MypyConfig = MypyConfig(),
    ) -> list[str]:
        
        hooks = [
            f'--{hook}' for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        
        return hooks
    
    @override
    def create_file_text (
        self,
        config: MypyConfig = MypyConfig(),
    ) -> str:
        
        hooks = self.generate_args(config)
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': {
                        'id': 'mypy',
                        'args': hooks,
                    },
                }
            ]
        }
    
    @override
    def create_file (
        self,
    ) -> None:
        
        text_dump = MypyCreator.prepare_text_dump()
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        if not pre_commit_file.exists():
            MypyCreator.create(text_dump)
        else:
            MypyCreator.update(text_dump)
    
    @override
    def prepare_text_dump (
        self,
    ) -> dict[str, Any]:
        
        config = MypyConfig(self.options)
        text = MypyCreator.create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        self.create_file()
        