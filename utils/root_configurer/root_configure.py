"""
RootConfigurer module.

This module defines a utility class for setting the project's root directory
as the current working directory and ensuring it is present in `sys.path`
for module imports.
"""

import os
import sys

from utils.static.privacy.privacy import privatemethod


class RootConfigurer:
    
    """
    RootConfigurer is responsible for configuring the project root directory.

    It changes the current working directory to the project root and ensures
    that the root is included in `sys.path` to allow absolute imports.
    """

    @privatemethod
    def _set_root (
        self,
    ) -> None:
        
        """
        Set the project root directory as the current working directory
        and add it to sys.path if not already present.
        """
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

        os.chdir(project_root)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

    def config (
        self,
    ) -> None:
        
        """
        Run the full root configuration process.
        """
        
        self._set_root()
