"""
Elasticsearch Config Creator Module

Provides functionality to generate and write an Elasticsearch configuration file
based on user-defined options.
"""

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.elk.elasticsearch.elasticsearch_config.elasticsearch_config import ElasticsearchConfig


class ElasticsearchConfigCreator(FileCreator):
    
    """
    Creates an Elasticsearch configuration file from provided options.
    """
    
    @staticmethod
    def create_file_text (
        config: ElasticsearchConfig = ElasticsearchConfig(),
    ) -> str:
        
        """
        Generates the Elasticsearch configuration as a string.

        :param cluster_name: Name of the Elasticsearch cluster.
        :param network_host: Network host setting (e.g., "0.0.0.0" to listen on all interfaces).
        :param discovery_type: Discovery type (e.g., "single-node" for local development).
        :return: A string containing the Elasticsearch configuration.
        """
        
        configuration = f"""cluster.name: "{config.cluster_name}"
network.host: {config.network_host}
discovery.type: {config.discovery_type}
"""
        return configuration

    @staticmethod
    def create_file (
        **options,
    ) -> None:
        
        """
        Writes the generated Elasticsearch configuration to a file.

        :param file_path: Path to the file where the configuration should be written.
        :param cluster_name: Name of the Elasticsearch cluster.
        :param network_host: Network host setting.
        :param discovery_type: Discovery type.
        """
        
        config = ElasticsearchConfig(**options)
        
        configuration = ElasticsearchConfigCreator.create_file_text (
            config,
        )
        with open('config/elk/elasticsearch.yml', "w") as f:
            f.write(configuration)     