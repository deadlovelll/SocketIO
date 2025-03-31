import yaml

from pathlib import Path

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_config.pre_commit_hooks_config import PreCommitHooksConfig

class PreCommitHooksCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        config: PreCommitHooksConfig = PreCommitHooksConfig(),
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
        
        yaml_dump = PreCommitHooksCreator.prepare_yaml_dump (
            **options,    
        )
        pre_commit_file = Path('../.pre-commit-config.yaml')
        
        if pre_commit_file.exists():
            PreCommitHooksCreator.create(yaml_dump)
        else:
            PreCommitHooksCreator.create(yaml_dump)
            
    @staticmethod
    def create (
        yaml_dump,
    ) -> None:
                
        with open('.pre-commit-config.yaml', 'w') as f:
            f.write(yaml_dump)
            
        print(f'.pre-commit-config.yaml has been created.')
        
    @staticmethod
    def update (
        new_config: PreCommitHooksConfig,
    ) -> None:
        
        new_config = new_config.__dict__
        
        with open('.pre-commit-config.yaml', "r") as f:
            config = yaml.safe_load(f) or {}
        
        config.setdefault('repos', [])
        
    @staticmethod
    def prepare_yaml_dump (
        **options,
    ) -> str:
        
        config = PreCommitHooksConfig(**options)
        text = PreCommitHooksCreator.create_file_text(config)
        yaml_dump = yaml.dump (
            text, 
            default_flow_style=False, 
            sort_keys=False,
        )
        
        return yaml_dump
        