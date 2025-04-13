from pathlib import Path

from typing import override, Any

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.black.black_config.black_config import BlackConfig

from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator


class BlackCreator(BaseHookCreator, FileCreator):
    
    def __init__ (
        self, 
        **options,
    ) -> None:
        
        super().__init__(**options)
        
        self.file_map = {
            True: super().create,
            False: super().update,
        }
        self.flag_map = {
            'skip_string_normalization': '--skip-string-normalization',
            'skip_magic_trailing_comma': '--skip-magic-trailing-comma',
            'check': '--check',
            'diff': '--diff',
            'preview': '--preview',
            'verbose': '--verbose',
            'quiet': '--quiet',
            'fast': '--fast',
        }
    
    @override
    def generate_args (
        self,
        config: BlackConfig,
    ) -> list[str]:
        
        args = [
            f'--line-length={config.line_length}',
            f'--target-version={config.target_version}',
        ]

        for attr, flag in self.flag_map.items():
            if getattr(config, attr):
                args.append(flag)

        return args
    
    @override
    def create_file_text (
        self,
        config: BlackConfig = BlackConfig(),
    ) -> str:
        
        hooks = self.generate_args(config)
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': {
                        'id': 'black',
                        'args': hooks
                    },
                },
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
        
        config = BlackConfig(**self.options)
        text = self.create_file_text(config)
        
        return text
    
    @override
    def execute (
        self,
    ) -> None:
        
        self.create_file()
        