"""
Elasticsearch Configuration Module

This module defines the `ElasticsearchConfig` dataclass, which holds configuration
parameters for setting up an Elasticsearch instance, typically in a Docker environment.
"""

from dataclasses import dataclass


@dataclass
class ElasticsearchConfig:
    
    """
    Dataclass to encapsulate configuration settings for Elasticsearch.

    Attributes:
        cluster_name (str): The name of the Elasticsearch cluster. Defaults to "docker-cluster".
        network_host (str): The network interface for Elasticsearch to bind to. Defaults to "0.0.0.0".
        discovery_type (str): The discovery type for Elasticsearch clustering. Defaults to "single-node".
    """
    
    cluster_name: str = 'docker-cluster'
    network_host: str = '0.0.0.0'
    discovery_type: str = 'single-node'
