import yaml

from pathlib import Path

from typing import override

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.black.black_config.black_config import BlackConfig

from commands.git.pre_commit.base.base_hook_creator import BaseHookCreator

class BlackCreator(BaseHookCreator, FileCreator):
    
    @staticmethod
    @override
    def generate_args (
        config: BlackConfig,
    ) -> list[str]:
        
        args = [
            f'--line-length={config.line_length}',
            f'--target-version={config.target_version}',
        ]

        flag_map = {
            'skip_string_normalization': '--skip-string-normalization',
            'skip_magic_trailing_comma': '--skip-magic-trailing-comma',
            'check': '--check',
            'diff': '--diff',
            'preview': '--preview',
            'verbose': '--verbose',
            'quiet': '--quiet',
            'fast': '--fast',
        }

        for attr, flag in flag_map.items():
            if getattr(config, attr):
                args.append(flag)

        return args
    
    @staticmethod
    @override
    def create_file_text (
        config: BlackConfig = BlackConfig(),
    ) -> str:
        
        hooks = BlackCreator.generate_args(config)
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
    
    @staticmethod
    @override
    def create_file (
        **options,
    ) -> None:
        
        text_dump = BlackCreator.prepare_text_dump (
            **options,    
        )
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        if not pre_commit_file.exists():
            BaseHookCreator.create(text_dump)
        else:
            BaseHookCreator.update(text_dump)
        
    @staticmethod
    @override
    def prepare_text_dump (
        **options,
    ) -> dict:
        
        config = BlackConfig(**options)
        text = BlackCreator.create_file_text(config)
        
        return text
        