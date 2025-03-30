import yaml

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.git_commands.pre_commit.pre_commit_hooks.pre_commit_hooks_config.pre_commit_hooks_config import PreCommitHooksConfig

class PreCommitHooksBuilder(FileCreator):
    
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
        
        config = PreCommitHooksConfig(**options)
        with open('.pre-commit-config.yaml', 'w') as f:
            yaml.dump (
                config, 
                f, 
                default_flow_style=False, 
                sort_keys=False,
            )
        print(f'.pre-commit-config.yaml has been created.')