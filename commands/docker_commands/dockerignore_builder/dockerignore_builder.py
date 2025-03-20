from commands.docker_commands.docker_definers.dockerignore_definers.dockerifnore_definers import (
    PythonCacheDefiner,
    VenvDefiner,
    SystemSpecsDefiner,
    LogsDefine,
    TestCoverageDefiner,
    GitAttributesDefiner,
    DockerFilesDefiner,
    PoetryDefiner,
    CompiledFiledDefiner,
    DocumentationDefiner,
    EnvFilesDefiner
)

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
        documentation,
        env_files: bool,
    ) -> str:
        
        python_caches = PythonCacheDefiner.define(python_cache)
        virtual_envs = VenvDefiner.define(virtual_environment)
        system_specs_files = SystemSpecsDefiner.define(system_spec_files)
        log = LogsDefine.define(logs)
        test_coverages = TestCoverageDefiner.define(test_coverage)
        git_attributes = GitAttributesDefiner.define(git)
        docker_files = DockerFilesDefiner.define(docker)
        poetry_file = PoetryDefiner.define(poetry)
        comp_files = CompiledFiledDefiner.define(compiled_files)
        docs = DocumentationDefiner.define(documentation)
        env_files = EnvFilesDefiner.define(env_files)