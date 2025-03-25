from SocketIO.interfaces.file_creator_interface.file_creator_interface import FileCreator

class LogstashConfigCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        beats_port: int = 5000,
        elasticsearch_host: str = "elasticsearch:9200",
        index_pattern: str = "logstash-%{+YYYY.MM.dd}",
    ) -> str:
        
        """
        Generates the Logstash configuration as a string.

        :param beats_port: Port on which Logstash listens for beats input.
        :param elasticsearch_host: Host (and port) for Elasticsearch.
        :param index_pattern: Index pattern for Elasticsearch output.
        :return: A string containing the Logstash configuration.
        """
        
        config = f"""input {{
  beats {{
    port => {beats_port}
  }}
}}

filter {{
  date {{
    match => [ "timestamp", "ISO8601" ]
    target => "@timestamp"
  }}
}}

output {{
  elasticsearch {{
    hosts => ["{elasticsearch_host}"]
    index => "{index_pattern}"
  }}
}}
"""
        return config

    @staticmethod
    def create_file (
        beats_port: int = 5000,
        elasticsearch_host: str = "elasticsearch:9200",
        index_pattern: str = "logstash-%{{+YYYY.MM.dd}}",
    ) -> None:
        
        """
        Writes the generated Logstash configuration to a file.

        :param beats_port: Port on which Logstash listens for beats input.
        :param elasticsearch_host: Host (and port) for Elasticsearch.
        :param index_pattern: Index pattern for Elasticsearch output.
        """
        
        config = LogstashConfigCreator.create_file_text (
            beats_port, 
            elasticsearch_host, 
            index_pattern,
        )
        with open('config/elk/logstash.conf', 'w') as f:
            f.write(config)