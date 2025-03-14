import textwrap

class DockerFileCreator:
    
    @staticmethod   
    def create_dockerfile(
        dockerfile_name: str = "Dockerfile",
        poetry: bool = True,
        python_version: str = "latest",
        use_alpine: bool = False,
        install_system_deps: bool = True,
        ports: list[int] = [4000],
        entrypoint: str = "main.py",
        use_nonroot_user: bool = True,
        grpc_enabled: bool = False
    ) -> None:
        
        """Generate a customizable Dockerfile for the framework."""
        
        # Select base image
        base_image = DockerFileCreator.define_python_version (
            python_version,
            use_alpine,
        )

        # Define exposed ports
        exposed_ports = DockerFileCreator.define_exposed_ports (
            ports,
            grpc_enabled,
        )
        
        # System dependencies installation (optional)
        system_deps = DockerFileCreator.define_system_deps (
            install_system_deps,
        )
        
        poetry_install = DockerFileCreator.define_poetry (
            poetry,
        )

        # Non-root user security (optional)
        user_security = DockerFileCreator.define_user_security (
            use_nonroot_user,
        )

        with open(f'./{dockerfile_name}', 'w') as file:
            file.write(dockerfile_content)

        print(f"Dockerfile '{dockerfile_name}' has been created.")
        
    @staticmethod
    def define_python_version (
        python_version: str, 
        use_alpine: bool,
    ) -> str:
        
        base_image = f"python:{python_version}"
        if use_alpine:
            base_image += '-alpine'
        return base_image

    @staticmethod
    def define_exposed_ports (
        ports,
        grpc_enabled,
    ) -> str:
        
        exposed_ports = "\n".join([f"EXPOSE {port}" for port in ports])
        if grpc_enabled:
            exposed_ports += "\nEXPOSE 50051"
        return exposed_ports
    
    @staticmethod
    def define_system_deps (
        install_system_deps,
    ) -> str:
        
        system_deps = ""
        if install_system_deps:
            system_deps = """
            RUN apt-get update && apt-get install -y --no-install-recommends \\
                build-essential \\
                && rm -rf /var/lib/apt/lists/*
            """
        return system_deps
    
    @staticmethod
    def define_poetry(poetry) -> str:
        poetry_install = ""
        if poetry:
            poetry_install = """
            ENV POETRY_HOME="/opt/poetry"
            ENV PATH="$POETRY_HOME/bin:$PATH"
            RUN pip install --upgrade pip setuptools wheel && \\
                pip install poetry && \\
                poetry config virtualenvs.create false && \\
                poetry install --no-dev --no-interaction --no-ansi --no-root
            """
        return poetry_install
    
    @staticmethod
    def define_user_security (
        use_nonroot_user,
    ) -> str:
        
        user_security = ""
        if use_nonroot_user:
            user_security = """
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
            """
        return user_security
    
    @staticmethod
    def define_dockkerfile_content (
        base_image,
        system_deps,
        poetry_install,
        user_security,
        exposed_ports,
        entrypoint,
    ) -> str:
        
        # Dockerfile content
        dockerfile_content = textwrap.dedent(f"""\
            # Stage 1: Build stage
            FROM {base_image} AS builder

            # Set work directory
            WORKDIR /app

            {system_deps}

            # Install dependencies
            COPY pyproject.toml poetry.lock ./
            {poetry_install}

            # Copy application files
            COPY . .

            # Stage 2: Final image
            FROM {base_image} AS final

            # Set work directory
            WORKDIR /app

            # Copy from the build stage
            COPY --from=builder / /

            {user_security}

            # Expose ports
            {exposed_ports}

            # Start the framework
            CMD ["python", "{entrypoint}"]
        """)
        
        return dockerfile_content