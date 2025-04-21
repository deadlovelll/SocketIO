"""
Logstash Configuration Data Model

This module defines the configuration structure used for generating
the `logstash.conf` file for a Logstash service.
"""

from dataclasses import dataclass


@dataclass
class LogstashConfig:
    
    """
    Data class representing configuration parameters for Logstash.

    Attributes:
        beats_port (int): The port on which Logstash will listen for Filebeat or other Beats data.
        elasticsearch_host (str): The host and port of the Elasticsearch instance where logs will be sent.
        index_pattern (str): The naming pattern for log indices created in Elasticsearch.
    """
    
    beats_port: int = 5000
    elasticsearch_host: str = 'elasticsearch:9200'
    index_pattern: str = 'logstash-%{{+YYYY.MM.dd}}'
