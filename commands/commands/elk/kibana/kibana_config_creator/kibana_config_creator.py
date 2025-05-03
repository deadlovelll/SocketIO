"""
Kibana Configuration Creator Module

This module defines a class responsible for generating and writing
a `kibana.yml` configuration file based on the provided configuration options.
"""

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.commands.elk.kibana.kibana_config.kibana_config import KibanaConfig


class KibanaConfigCreator(FileCreator):
    
    """
    Creates a `kibana.yml` configuration file based on the specified `KibanaConfig`.

    This includes Elasticsearch connection settings, Kibana server host/port, 
    and authentication options if provided.
    """
    
    @staticmethod
    def create_file_text (
        config: KibanaConfig = KibanaConfig(),
    ) -> str:
        
        """
        Generates the Kibana configuration as a string.

        Args:
            config (KibanaConfig): Configuration parameters for Kibana.

        Returns:
            str: A string representing the contents of the `kibana.yml` file.
        """
        
        configuration = f"""server.host: "{config.server_host}"
server.port: {config.server_port}
elasticsearch.hosts: ["{config.elasticsearch_host}"]
kibana.index: "{config.kibana_index}"
"""

        if config.elasticsearch_username and config.elasticsearch_password:
            configuration += f"""elasticsearch.username: "{config.elasticsearch_username}"
elasticsearch.password: "{config.elasticsearch_password}"
"""

        return configuration

    @staticmethod
    def create_file (
        **options,
    ) -> None:
        
        """
        Writes the generated Kibana configuration to a file.

        Args:
            options (dict): Keyword arguments that match the fields of KibanaConfig.

        Returns:
            None
        """
        
        config = KibanaConfig(**options)
        
        configuration = KibanaConfigCreator.create_file_text (
            config,
        )
        
        with open('config/elk/kibana.yml', "w") as f:
            f.write(configuration)