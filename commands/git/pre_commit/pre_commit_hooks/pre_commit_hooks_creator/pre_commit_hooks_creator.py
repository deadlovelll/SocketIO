import yaml

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
        
        config = PreCommitHooksConfig(**options)
        text = PreCommitHooksCreator.create_file_text(config)
        with open('.pre-commit-config.yaml', 'a+') as f:
            yaml.dump (
                text, 
                f, 
                default_flow_style=False, 
                sort_keys=False,
            )
        print(f'.pre-commit-config.yaml has been created.')