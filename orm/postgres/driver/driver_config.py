from dataclasses import dataclass

@dataclass
class PostgresDriverConfig:
    host: str
    port: int
    user: str
    password: str
    database_name: str