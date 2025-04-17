import os
import sys

class RootConfigurer:
    
    def set_root (
        self,
    ) -> None:
        
        project_root = os.path.dirname (
            os.path.abspath(os.path.join(__file__, '../../'))
        )
        
        os.chdir(project_root)
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
    
    def config (
        self,
    ) -> None:
        
        self.set_root()