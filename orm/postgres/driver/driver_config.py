from dataclasses import dataclass

@dataclass
class PostgresDriverConfig:
    host: str = 'localhost'
    port: int = 5432
    user: str = 'posgtres'
    password: str = 'posgtres'
    database_name: str = 'postgres'