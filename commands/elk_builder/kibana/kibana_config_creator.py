from interfaces.file_creator_interface.file_creator_interface import FileCreator

class KibanaConfigCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        server_host: str = "0.0.0.0",
        server_port: int = 5601,
        elasticsearch_host: str = "http://elasticsearch:9200",
        elasticsearch_username: str = "",
        elasticsearch_password: str = "",
        kibana_index: str = ".kibana",
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
        
        config = f"""server.host: "{server_host}"
server.port: {server_port}
elasticsearch.hosts: ["{elasticsearch_host}"]
kibana.index: "{kibana_index}"
"""

        if elasticsearch_username and elasticsearch_password:
            config += f"""elasticsearch.username: "{elasticsearch_username}"
elasticsearch.password: "{elasticsearch_password}"
"""

        return config

    @staticmethod
    def create_file (
        server_host: str = "0.0.0.0",
        server_port: int = 5601,
        elasticsearch_host: str = "http://elasticsearch:9200",
        elasticsearch_username: str = "",
        elasticsearch_password: str = "",
        kibana_index: str = ".kibana",
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
        
        config = KibanaConfigCreator.create_file_text (
            server_host, 
            server_port, 
            elasticsearch_host, 
            elasticsearch_username, 
            elasticsearch_password, 
            kibana_index,
        )
        
        with open('config/elk/kibana.yml', "w") as f:
            f.write(config)