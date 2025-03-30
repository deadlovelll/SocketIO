from dataclasses import dataclass, field
from typing import List, Optional

import requests

@dataclass
class PreCommitHooksConfig:
    url: str = field (
        init=False, 
        default='https://github.com/pre-commit/pre-commit-hooks'
    )
    rev: str = field (
        default_factory=lambda: PreCommitHooksConfig.get_latest_version()
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
    
    @staticmethod
    def get_latest_version() -> str:
        
        api_url = "https://api.github.com/repos/pre-commit/pre-commit-hooks/releases/latest"
        
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            return response.json().get('tag_name')
        
        except (requests.RequestException, KeyError):
            print("Warning: Failed to fetch required version. Using default version v4.0.1")
            return "v4.0.1"