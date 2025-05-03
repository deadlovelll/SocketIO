"""
Logstash Configuration Creator

This module defines the `LogstashConfigCreator` class used to generate
a valid `logstash.conf` configuration file for Logstash based on user-defined options.
"""

from interfaces.file_creator_interface.file_creator_interface import FileCreator
from commands.commands.elk.logstash.logstash_config.logstash_config import LogstashConfig

class LogstashConfigCreator(FileCreator):
  
    """
    Logstash configuration file creator.

    This class provides static methods for generating and writing
    a valid `logstash.conf` file with input, filter, and output stages,
    tailored for use with Filebeat and Elasticsearch.
    """
    
    @staticmethod
    def create_file_text(
        config: LogstashConfig = LogstashConfig(),
    ) -> str:
      
        """
        Generates the Logstash configuration as a string.

        Args:
            config (LogstashConfig): The configuration dataclass for Logstash.

        Returns:
            str: A formatted Logstash configuration file content.
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
    def create_file(
        **options,
    ) -> None:
      
        """
        Writes the generated Logstash configuration to `config/elk/logstash.conf`.

        Args:
            **options: Arbitrary keyword arguments used to initialize `LogstashConfig`.

        Returns:
            None
        """
        
        config = LogstashConfig(**options)
        content = LogstashConfigCreator.create_file_text(config)

        with open('config/elk/logstash.conf', 'w') as f:
            f.write(content)