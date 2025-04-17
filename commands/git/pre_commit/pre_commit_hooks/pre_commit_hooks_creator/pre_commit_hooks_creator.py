from pathlib import Path
from typing import Any, override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_config.pre_commit_hooks_config import PreCommitHooksConfig


class PreCommitHooksCreator(BaseHookCreator, FileCreator):
        
    @override
    def generate_args (
        self,
        config: PreCommitHooksConfig = PreCommitHooksConfig(),
    ) -> list[str]:
        
        hooks = [
            {'id': hook} for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        
        return hooks
    
    @override
    def create_file_text (
        self,
        config: PreCommitHooksConfig = PreCommitHooksConfig(),
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
        
        config = PreCommitHooksConfig(**self.options)
        text = self.create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        self.create_file()
        