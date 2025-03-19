from commands.docker_commands.docker_definers.base_definer.base_definer import BaseDockerDefiner

class PythonCacheDefiner(BaseDockerDefiner):
    
    @staticmethod
    def define (
        python_cache: bool,
    ) -> str:
        
        if python_cache:
            return "\n".join([
                "__pycache__/",
                "*.pyc",
                "*.pyo",
                "*.pyd",
            ])
        return ""