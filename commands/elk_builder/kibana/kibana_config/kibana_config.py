from dataclasses import dataclass

@dataclass
class KibanaConfig:
    server_host: str = "0.0.0.0",
    server_port: int = 5601,
    elasticsearch_host: str = "http://elasticsearch:9200",
    elasticsearch_username: str = "",
    elasticsearch_password: str = "",
    kibana_index: str = ".kibana",