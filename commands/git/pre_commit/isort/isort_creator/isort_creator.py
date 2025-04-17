from pathlib import Path
from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.isort.isort_config.isort_config import IsortConfig
from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator


class IsortCreator(BaseHookCreator, FileCreator):
        
    @override
    def generate_args (
        self,
        config: IsortConfig = IsortConfig(),
    ) -> list[str]:
        
        hooks = [
            {'id': hook} for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        
        return hooks
    
    @override
    def create_file_text (
        self,
        config: IsortConfig = IsortConfig(),
    ) -> str:
        
        hooks = self.generate_args(config)
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': hooks,
                }
            ]
        }
    
    @override
    def create_file (
        self,
    ) -> None:
        
        text_dump = self.prepare_text_dump()
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        file_exist = pre_commit_file.exists()
        self.file_map[file_exist](text_dump)
    
    @override
    def prepare_text_dump (
        self,
    ) -> dict[str, Any]:
        
        config = IsortConfig(**self.options)
        text = self.create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        self.create_file()
        