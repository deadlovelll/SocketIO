import os

from commands.elk_builder.elasticsearch.elasticseacrh_config_creator import ElasticsearchConfigCreator
from commands.elk_builder.kibana.kibana_config_creator import KibanaConfigCreator
from commands.elk_builder.logstash.logstash_config_creator import LogstashConfigCreator

class ELKConfigCreator:
    
    @staticmethod
    def create_elk_config():
        
        config_path = "config/elk"
        os.makedirs(config_path, exist_ok=True) 

        ElasticsearchConfigCreator.write_config()
        LogstashConfigCreator.write_config()
        KibanaConfigCreator.write_config()
        
        print('elk config created successfully!')