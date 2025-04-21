"""
Kibana Configuration Data Class

This dataclass defines the configuration parameters required for generating
a `kibana.yml` configuration file used to configure the Kibana service.
"""

from dataclasses import dataclass


@dataclass
class KibanaConfig:
    
    """
    Represents configuration options for Kibana.

    Attributes:
        server_host (str): The network address Kibana will bind to.
        server_port (int): The port number Kibana will listen on.
        elasticsearch_host (str): The URL to the Elasticsearch service.
        elasticsearch_username (str): Optional username for Elasticsearch authentication.
        elasticsearch_password (str): Optional password for Elasticsearch authentication.
        kibana_index (str): Index used to store Kibana settings and saved objects.
    """
    
    server_host: str = "0.0.0.0"
    server_port: int = 5601
    elasticsearch_host: str = "http://elasticsearch:9200"
    elasticsearch_username: str = ""
    elasticsearch_password: str = ""
    kibana_index: str = ".kibana"
