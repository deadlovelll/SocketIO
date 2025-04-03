import yaml

from pathlib import Path
from typing import Any

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.isort.isort_config.isort_config import IsortConfig


class IsortCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        config: IsortConfig = IsortConfig(),
    ) -> str:
        
        hooks = [
            {'id': hook} for hook, enabled in config.__dict__.items()
            if isinstance(enabled, bool) and enabled
        ]
        return {
            'repos': [
                {
                    'repo': config.url, 
                    'rev': config.rev, 
                    'hooks': hooks,
                }
            ]
        }
    
    @staticmethod
    def create_file (
        **options,
    ) -> None:
        
        text_dump = IsortCreator.prepare_text_dump (
            **options,    
        )
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        if not pre_commit_file.exists():
            IsortCreator.create(text_dump)
        else:
            IsortCreator.update(text_dump)
            
    @staticmethod
    def create (
        text_dump: str,
    ) -> None:
                
        with open('.pre-commit-config.yaml', 'w') as f:
            yaml.dump (
                text_dump, 
                f,
                default_flow_style=False, 
                sort_keys=False,
            )
            
        print(f'.pre-commit-config.yaml has been created.')
        
    @staticmethod
    def update (
        text_dump: dict[str, Any],
    ) -> None:
        
        with open('.pre-commit-config.yaml', 'r') as f:
            config = yaml.safe_load(f) or {}
        
        config.setdefault('repos', [])
        
        updated = False
        for i, repo in enumerate(config['repos']):
            if repo.get('repo') == text_dump.get('repo'):
                config['repos'][i] = text_dump
                updated = True
                break

        if not updated:
            config['repos'].append(text_dump)

        with open('.pre-commit-config.yaml', 'w') as f:
            yaml.dump (
                config, 
                f, 
                default_flow_style=False, 
                sort_keys=False,
            )
        
    @staticmethod
    def prepare_text_dump (
        **options,
    ) -> dict:
        
        config = IsortConfig(**options)
        text = IsortCreator.create_file_text(config)
        
        return text
        