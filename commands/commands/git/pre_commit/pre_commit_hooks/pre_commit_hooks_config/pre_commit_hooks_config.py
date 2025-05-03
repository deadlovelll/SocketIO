"""
This module defines the PreCommitHooksConfig dataclass, which is used to
configure the built-in hook set provided by the official `pre-commit-hooks` repository.

The configuration allows enabling or disabling specific hooks such as
trailing whitespace trimming, YAML/JSON validation, debug statement detection, etc.
"""

from dataclasses import dataclass, field

from commands.commands.git.last_release_fetcher.last_release_fetcher import LastReleaseFetcher


@dataclass
class PreCommitHooksConfig:
    
    """
    Configuration class for enabling or disabling individual hooks from
    the `pre-commit-hooks` repository.

    Attributes:
        url (str): URL of the `pre-commit-hooks` GitHub repository.
        rev (str): Specific version of the repository to pin the hooks to.
        trailing_whitespace (bool): Enables `trailing-whitespace` hook.
        end_of_file_fixer (bool): Enables `end-of-file-fixer` hook.
        check_yaml (bool): Enables `check-yaml` hook.
        check_json (bool): Enables `check-json` hook.
        debug_statements (bool): Enables `debug-statements` hook.
        check_merge_conflict (bool): Enables `check-merge-conflict` hook.
        mixed_line_ending (bool): Enables `mixed-line-ending` hook.
        check_case_conflict (bool): Enables `check-case-conflict` hook.
        check_symlinks (bool): Enables `check-symlinks` hook.
        requirements_txt_fixer (bool): Enables `requirements-txt-fixer` hook.
        check_added_large_files (bool): Enables `check-added-large-files` hook.
        check_ast (bool): Enables `check-ast` hook.
        check_builtin_literals (bool): Enables `check-builtin-literals` hook.
        check_docstring_first (bool): Enables `check-docstring-first` hook.
        check_executables_have_shebangs (bool): Enables `check-executables-have-shebangs` hook.
        check_toml (bool): Enables `check-toml` hook.
        check_vcs_permalinks (bool): Enables `check-vcs-permalinks` hook.
        check_xml (bool): Enables `check-xml` hook.
        fix_byte_order_marker (bool): Enables `fix-byte-order-marker` hook.
        name_tests_test (bool): Enables `name-tests-test` hook.
        pretty_format_json (bool): Enables `pretty-format-json` hook.
    """
    
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
    
    def __post_init__ (
        self,
    ) -> None:
        
        """
        Fetches the latest version (tag) of the `pre-commit-hooks` repository
        after the dataclass is initialized and assigns it to `rev`.
        """
        
        owner_repo = self.url.split("https://github.com/")[1]
        self.rev = LastReleaseFetcher.fetch(owner_repo)