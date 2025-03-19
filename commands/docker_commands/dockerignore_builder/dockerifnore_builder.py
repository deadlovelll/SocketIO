from commands.docker_commands.dockerignore_builder.definers.python_cache_definer.python_cache_definer import PythonCacheDefiner

class DockerignoreBuilder:
    
    def create_dockerignorefile (
        python_cache: bool,
        virtual_environment: bool,
        system_spec_files: bool,
        logs: bool,
        test_coverage: bool,
        git: bool,
        docker: bool,
        poetry,
        compiled_files: bool,
        grpc: bool,
        documnetation,
        env_files: bool,
    ):
        python_caches = PythonCacheDefiner.define(python_cache)