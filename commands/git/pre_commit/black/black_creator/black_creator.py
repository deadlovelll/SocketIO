import yaml

from pathlib import Path

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.black.black_config.black_config import BlackConfig


class BlackCreator(FileCreator):
    
    @staticmethod
    def generate_black_args (
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
    def create_file_text (
        config: BlackConfig = BlackConfig(),
    ) -> str:
        
        hooks = BlackCreator.generate_black_args(config)
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
    def create_file (
        **options,
    ) -> None:
        
        text_dump = BlackCreator.prepare_text_dump (
            **options,    
        )
        root = Path(__file__).resolve().parents[6]
        pre_commit_file = root / '.pre-commit-config.yaml'
        
        if not pre_commit_file.exists():
            BlackCreator.create(text_dump)
        else:
            BlackCreator.update(text_dump)
            
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
        text_dump: dict,
    ) -> None:
        
        with open('.pre-commit-config.yaml', 'r') as f:
            config = yaml.safe_load(f) or {}
        
        config.setdefault('repos', [])
        
        updated = False
        for i, repo in enumerate(config['repos']):
            if repo.get('repo') == text_dump['repos'][0]['repo']:
                config['repos'][i] = text_dump['repos'][0]
                updated = True
                break

        if not updated:
            config['repos'].append(text_dump['repos'][0])

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
        
        config = BlackConfig(**options)
        text = BlackCreator.create_file_text(config)
        
        return text
        