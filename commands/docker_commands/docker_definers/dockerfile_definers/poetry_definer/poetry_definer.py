class PoetryDefiner:
    
    @staticmethod
    def define_poetry (
        poetry: bool, 
        in_env: bool,
    ) -> str:
        
        env_setup = """\
RUN python -m venv /venv && \\
    . /venv/bin/activate
""" if in_env else ""

        if poetry:
            return f"""\
{env_setup}COPY pyproject.toml poetry.lock ./
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel && \\
    pip install poetry && \\
    poetry config virtualenvs.create false && \\
    poetry install --no-dev --no-interaction --no-ansi --no-root
"""
        else:
            return f"""{env_setup}COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel && \\
    pip install -r requirements.txt
    """
