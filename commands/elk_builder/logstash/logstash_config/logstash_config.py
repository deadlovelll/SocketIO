from dataclasses import dataclass

@dataclass
class LogstashConfig:
    beats_port: int = 5000,
    elasticsearch_host: str = "elasticsearch:9200",
    index_pattern: str = "logstash-%{{+YYYY.MM.dd}}",