from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class MypyConfig:
    url: str = field(init=False, default="https://github.com/pre-commit/mirrors-mypy")
    rev: str = "v1.9.0" 

    config_file: Optional[str] = "mypy.ini" 
    python_version: Optional[str] = None     
    ignore_missing_imports: bool = True
    disallow_untyped_defs: bool = False
    strict_optional: bool = False
    check_untyped_defs: bool = True
    no_implicit_optional: bool = False
    show_error_codes: bool = True
    warn_unused_ignores: bool = True
    exclude: Optional[str] = None
    additional_args: List[str] = field(default_factory=list)