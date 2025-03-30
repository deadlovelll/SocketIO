from interfaces.file_creator_interface.file_creator_interface import FileCreator

from commands.elk.kibana.kibana_config.kibana_config import KibanaConfig

class KibanaConfigCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        config: KibanaConfig = KibanaConfig(),
    ) -> str:
        
        """
        Generates the Kibana configuration as a string.

        :param server_host: Host for the Kibana server (default: "0.0.0.0").
        :param server_port: Port for Kibana (default: 5601).
        :param elasticsearch_host: URL of the Elasticsearch instance.
        :param elasticsearch_username: Username for Elasticsearch authentication (optional).
        :param elasticsearch_password: Password for Elasticsearch authentication (optional).
        :param kibana_index: Kibana index name (default: ".kibana").
        :return: A string containing the Kibana configuration.
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

        :param file_path: Path to the file where the configuration should be written.
        :param server_host: Host for the Kibana server.
        :param server_port: Port for Kibana.
        :param elasticsearch_host: URL of the Elasticsearch instance.
        :param elasticsearch_username: Username for Elasticsearch authentication (optional).
        :param elasticsearch_password: Password for Elasticsearch authentication (optional).
        :param kibana_index: Kibana index name.
        """
        
        config = KibanaConfig(**options)
        
        configuration = KibanaConfigCreator.create_file_text (
            config,
        )
        
        with open('config/elk/kibana.yml', "w") as f:
            f.write(configuration)