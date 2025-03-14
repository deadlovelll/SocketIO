import textwrap

class DockerfileFactory:
    
    def __init__ (
        self,
        python_version: str = "latest",
        use_alpine: bool = False,
        install_system_deps: bool = True,
        poetry: bool = True,
        ports: list[int] = [4000],
        entrypoint: str = "main.py",
        use_nonroot_user: bool = True,
        grpc_enabled: bool = False,
    ) -> None:
        
        self.python_version = python_version
        self.use_alpine = use_alpine
        self.install_system_deps = install_system_deps
        self.poetry = poetry
        self.ports = ports
        self.entrypoint = entrypoint
        self.use_nonroot_user = use_nonroot_user
        self.grpc_enabled = grpc_enabled

    def create (
        self,
    ) -> str:
        
        return textwrap.dedent(f"""
            FROM {self._define_python_version()} AS builder

            WORKDIR /app

            {self._define_system_deps()}

            COPY pyproject.toml poetry.lock ./
            {self._define_poetry()}

            COPY . .

            FROM {self._define_python_version()} AS final

            WORKDIR /app
            COPY --from=builder / /

            {self._define_user_security()}
            {self._define_exposed_ports()}

            CMD ["python", "{self.entrypoint}"]
        """)

    def _define_python_version (
        self,
    ) -> str:
        
        return f"python:{self.python_version}{'-alpine' if self.use_alpine else ''}"

    def _define_exposed_ports (
        self,
    ) -> str:
        
        ports = "\n".join(f"EXPOSE {port}" for port in self.ports)
        if self.grpc_enabled:
            ports += "\nEXPOSE 50051"
        return ports

    def _define_system_deps (
        self,
    ) -> str:
        
        return textwrap.dedent("""
            RUN apt-get update && apt-get install -y --no-install-recommends \
                build-essential \
                && rm -rf /var/lib/apt/lists/*
        """) if self.install_system_deps else ""

    def _define_poetry (
        self,
    ) -> str:
        
        return textwrap.dedent("""
            ENV POETRY_HOME="/opt/poetry"
            ENV PATH="$POETRY_HOME/bin:$PATH"
            RUN pip install --upgrade pip setuptools wheel && \
                pip install poetry && \
                poetry config virtualenvs.create false && \
                poetry install --no-dev --no-interaction --no-ansi --no-root
        """) if self.poetry else ""

    def _define_user_security (
        self,
    ) -> str:
        
        return textwrap.dedent("""
            RUN useradd -m nonroot && chown -R nonroot:nonroot /app
            USER nonroot
        """) if self.use_nonroot_user else ""

    def create_dockerfile (
        self, 
        filename: str = "Dockerfile",
    ) -> None:
        
        with open(filename, "w") as f:
            f.write(self.create())
        print(f"Dockerfile '{filename}' has been created.")