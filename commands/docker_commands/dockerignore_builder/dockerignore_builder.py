import textwrap

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
    
    @staticmethod
    def create_dockerignorefile_text (
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
        env_file = EnvFilesDefiner.define(env_files)
        
        content = f"""
            {python_caches}
            {virtual_envs}
            {system_specs_files}
            {log}
            {test_coverages}
            {git_attributes}
            {docker_files}
            {poetry_file}
            {comp_files}
            {docs}
            {env_file}
        """
        
        return textwrap.dedent(content).strip()
    
    @staticmethod
    def create_dockerfile (
        python_cache: bool,
        virtual_environment: bool,
        system_spec_files: bool,
        logs: bool,
        test_coverage: bool,
        git: bool,
        docker: bool,
        poetry: bool,
        compiled_files: bool,
        documentation,
        env_files: bool,
    ) -> None:
        
        with open('.dockerignore', 'w') as f:
            f.write(DockerignoreBuilder.create_dockerignorefile_text (
                python_cache,
                virtual_environment,
                system_spec_files,
                logs,
                test_coverage,
                git,
                docker,
                poetry,
                compiled_files,
                documentation,
                env_files,
            ))
        print(f".dockerignore has been created.")