from interfaces.file_creator_interface.file_creator_interface import FileCreator

from commands.elk_builder.logstash.logstash_config.logstash_config import LogstashConfig

class LogstashConfigCreator(FileCreator):
    
    @staticmethod
    def create_file_text (
        config: LogstashConfig = LogstashConfig(),
    ) -> str:
        
        """
        Generates the Logstash configuration as a string.

        :param beats_port: Port on which Logstash listens for beats input.
        :param elasticsearch_host: Host (and port) for Elasticsearch.
        :param index_pattern: Index pattern for Elasticsearch output.
        :return: A string containing the Logstash configuration.
        """
        
        configuration = f"""input {{
  beats {{
    port => {config.beats_port}
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
    hosts => ["{config.elasticsearch_host}"]
    index => "{config.index_pattern}"
  }}
}}
"""
        return configuration

    @staticmethod
    def create_file (
        **options,
    ) -> None:
        
        """
        Writes the generated Logstash configuration to a file.

        :param beats_port: Port on which Logstash listens for beats input.
        :param elasticsearch_host: Host (and port) for Elasticsearch.
        :param index_pattern: Index pattern for Elasticsearch output.
        """
        
        config = LogstashConfig(**options)
        
        configuration = LogstashConfigCreator.create_file_text (
            config,
        )
        with open('config/elk/logstash.conf', 'w') as f:
            f.write(configuration)