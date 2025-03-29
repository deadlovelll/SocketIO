from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PreCommitConfig:
    pch: Optional[bool] = True
    pch_py_version: Optional[str]
    
    isort: Optional[bool] = True
    isort_py_version: Optional[str]
    
    black: Optional[bool] = True
    black_py_version: Optional[str]
    
    custom_linter: Optional[bool] = False
    cl_path: Optional[str] 
    