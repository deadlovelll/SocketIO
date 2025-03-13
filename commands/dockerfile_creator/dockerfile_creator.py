import textwrap

class DockerFileCreator:
    
    @staticmethod   
    def create_dockerfile (
        dockerfile_name: str,
    ) -> None:
        
        dockerfile_content = textwrap.dedent("""\
        # Stage 1: Build stage
        FROM python:lastest AS builder

        # Set work directory
        WORKDIR /app

        # Install system dependencies
        RUN apt-get update && apt-get install -y --no-install-recommends \
            build-essential \
            && rm -rf /var/lib/apt/lists/*

        # Set environment variables
        ENV PYTHONDONTWRITEBYTECODE=1
        ENV PYTHONUNBUFFERED=1
        ENV POETRY_HOME="/opt/poetry"
        ENV PATH="/root/.local/bin:$PATH"

        # Install dependencies
        COPY pyproject.toml poetry.lock ./
        RUN pip install --upgrade pip setuptools wheel && \
            pip install poetry && \
            poetry config virtualenvs.create false && \
            poetry install --no-dev --no-interaction --no-ansi --no-root

        # Copy application files
        COPY . .

        # Stage 2: Final image
        FROM python:lastest AS final

        # Set work directory
        WORKDIR /app

        # Copy from the build stage
        COPY --from=builder / /

        # Add a non-root user for security
        RUN useradd -m nonroot && chown -R nonroot:nonroot /app
        USER nonroot

        # Expose port
        EXPOSE 4000

        # Start the framework
        CMD ["python", "main.py", "start"]
        """)

        with open(f'./{dockerfile_name}', 'w') as file:
            file.write(dockerfile_content)

        print("Dockerfile has been created.")