from abc import abstractmethod
from commands.base_command.base_command import BaseCommand
from typing import Any

import yaml

class BaseHookCreator(BaseCommand):
    
    @abstractmethod
    def generate_args (
        config,
    ) -> list[str]:
        
        pass
    
    @abstractmethod
    def create_file_text (
        config,
    ) -> str:
        
        pass
    
    @abstractmethod
    def create_file (
        **options,
    ) -> None:
        
        pass
    
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
    
    def update (
        self,
        text_dump: dict[str, Any],
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
    
    @abstractmethod
    def prepare_text_dump (
        **options,
    ) -> dict[str, Any]:
        
        pass