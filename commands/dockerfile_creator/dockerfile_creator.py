import textwrap

class DockerfileFactory:

    @staticmethod
    def create (
        python_version: str = "latest",
        use_alpine: bool = False,
        install_system_deps: bool = True,
        poetry: bool = True,
        ports: list[int] = [4000],
        entrypoint: str = "main.py",
        use_nonroot_user: bool = True,
        grpc_enabled: bool = False,
    ) -> str:
        
        return textwrap.dedent(f"""
            FROM {DockerfileFactory._define_python_version(python_version, use_alpine)} AS builder

            WORKDIR /app

            {DockerfileFactory._define_system_deps(install_system_deps)}

            COPY pyproject.toml poetry.lock ./
            {DockerfileFactory._define_poetry(poetry)}

            COPY . .

            FROM {DockerfileFactory._define_python_version(python_version, use_alpine)} AS final

            WORKDIR /app
            COPY --from=builder / /

            {DockerfileFactory._define_user_security(use_nonroot_user)}
            {DockerfileFactory._define_exposed_ports(ports, grpc_enabled)}

            CMD ["python", "{entrypoint}"]
        """)

    @staticmethod
    def _define_python_version (
        python_version: str, 
        use_alpine: bool,
    ) -> str:
        
        return f"python:{python_version}{'-alpine' if use_alpine else ''}"

    @staticmethod
    def _define_exposed_ports (
        ports: list[int], 
        grpc_enabled: bool,
    ) -> str:
        
        ports = "\n".join(f"EXPOSE {port}" for port in ports)
        if grpc_enabled:
            ports += "\nEXPOSE 50051"
        return ports

    @staticmethod
    def _define_system_deps (
        install_system_deps: bool,
    ) -> str:
        
        return textwrap.dedent("""
            RUN apt-get update && apt-get install -y --no-install-recommends \
                build-essential \
                && rm -rf /var/lib/apt/lists/*
        """) if install_system_deps else ""

    @staticmethod
    def _define_poetry (
        poetry: bool,
    ) -> str:
        
        return textwrap.dedent("""
            ENV POETRY_HOME="/opt/poetry"
            ENV PATH="$POETRY_HOME/bin:$PATH"
            RUN pip install --upgrade pip setuptools wheel && \
                pip install poetry && \
                poetry config virtualenvs.create false && \
                poetry install --no-dev --no-interaction --no-ansi --no-root
        """) if poetry else ""

    @staticmethod
    def _define_user_security (
        use_nonroot_user: bool,
    ) -> str:
        
        return textwrap.dedent("""
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
        """) if use_nonroot_user else ""

    @staticmethod
    def create_dockerfile (
        filename: str = "Dockerfile",
        python_version: str = "latest",
        use_alpine: bool = False,
        install_system_deps: bool = True,
        poetry: bool = True,
        ports: list[int] = [4000],
        entrypoint: str = "main.py",
        use_nonroot_user: bool = True,
        grpc_enabled: bool = False,
    ) -> None:
        
        with open(filename, "w") as f:
            f.write(DockerfileFactory.create (
                python_version, 
                use_alpine, 
                install_system_deps, 
                poetry, 
                ports, 
                entrypoint, 
                use_nonroot_user, 
                grpc_enabled,
            ))
        print(f"Dockerfile '{filename}' has been created.")