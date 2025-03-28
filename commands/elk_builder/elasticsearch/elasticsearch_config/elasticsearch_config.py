from dataclasses import dataclass

@dataclass
class ElastisearchConfig:
    cluster_name: str = "docker-cluster",
    network_host: str = "0.0.0.0",
    discovery_type: str = "single-node",