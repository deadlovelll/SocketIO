class PythonVesionDefiner:
    
    @staticmethod
    def define_python_version (
        python_version: str, 
        use_alpine: bool,
    ) -> str:
        
        return f"python:{python_version}{'-alpine' if use_alpine else ''}"