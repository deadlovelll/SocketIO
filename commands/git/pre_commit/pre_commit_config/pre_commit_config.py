from dataclasses import dataclass

@dataclass
class PreCommitConfig:
    black: bool
    isort: bool
    mypy: bool
    custom_linter: bool = False