from interfaces.file_creator_interface.file_creator_interface import FileCreator

class ElasticsearchConfigCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        cluster_name: str = "docker-cluster",
        network_host: str = "0.0.0.0",
        discovery_type: str = "single-node",
    ) -> str:
        
        """
        Generates the Elasticsearch configuration as a string.

        :param cluster_name: Name of the Elasticsearch cluster.
        :param network_host: Network host setting (e.g., "0.0.0.0" to listen on all interfaces).
        :param discovery_type: Discovery type (e.g., "single-node" for local development).
        :return: A string containing the Elasticsearch configuration.
        """
        
        config = f"""cluster.name: "{cluster_name}"
network.host: {network_host}
discovery.type: {discovery_type}
"""
        return config

    @staticmethod
    def create_file (
        cluster_name: str = "docker-cluster",
        network_host: str = "0.0.0.0",
        discovery_type: str = "single-node",
    ) -> None:
        
        """
        Writes the generated Elasticsearch configuration to a file.

        :param file_path: Path to the file where the configuration should be written.
        :param cluster_name: Name of the Elasticsearch cluster.
        :param network_host: Network host setting.
        :param discovery_type: Discovery type.
        """
        
        config = ElasticsearchConfigCreator.create_file_text (
            cluster_name, 
            network_host, 
            discovery_type,
        )
        with open('config/elk/elasticsearch.yml', "w") as f:
            f.write(config)     