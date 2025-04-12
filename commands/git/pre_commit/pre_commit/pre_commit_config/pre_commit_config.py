from dataclasses import dataclass

@dataclass
class PreCommitConfig:
    precommithooks: bool = True
    black: bool = True
    isort: bool = True
    mypy: bool = True
    custom_linter: bool = False