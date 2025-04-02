from dataclasses import dataclass, field
import requests

from commands.git.pre_commit.pre_commit_hooks.pre_commit_hooks_validator.pre_commit_hooks_validator import PreCommitHooksValidator
from commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher

@dataclass
class PreCommitHooksConfig:
    url: str = field (
        init=False, 
        default='https://github.com/pre-commit/pre-commit-hooks',
    )
    rev: str = field (
        init=False,
    )
    trailing_whitespace: bool = True
    end_of_file_fixer: bool = True
    check_yaml: bool = True
    check_json: bool = True
    debug_statements: bool = True
    check_merge_conflict: bool = True
    mixed_line_ending: bool = True
    check_case_conflict: bool = True
    check_symlinks: bool = True
    requirements_txt_fixer: bool = True
    check_added_large_files: bool = False
    check_ast: bool = False
    check_builtin_literals: bool = False
    check_docstring_first: bool = False
    check_executables_have_shebangs: bool = False
    check_toml: bool = False
    check_vcs_permalinks: bool = False
    check_xml: bool = False
    fix_byte_order_marker: bool = False
    name_tests_test: bool = False
    pretty_format_json: bool = False
    
    def __post_init__(self):
        owner_repo = self.url.split("https://github.com/")[1]
        self.rev = LastReleaseFetcher.fetch(owner_repo)