import os

from SocketIO.commands.elk_builder.elasticsearch.elasticseacrh_config_creator import ElasticsearchConfigCreator
from SocketIO.commands.elk_builder.kibana.kibana_config_creator import KibanaConfigCreator
from SocketIO.commands.elk_builder.logstash.logstash_config_creator import LogstashConfigCreator

class ELKConfigCreator:
    
    @staticmethod
    def create_elk_config():
        
        config_path = 'config/elk'
        os.makedirs(config_path, exist_ok=True) 

        services = {
            'Elasticsearch': ElasticsearchConfigCreator,
            'Logstash': LogstashConfigCreator,
            'Kibana': KibanaConfigCreator
        }

        for service_name, creator in services.items():
            try:
                config_file = creator.create_file(config_path)
            except Exception as e:
                pass
        
        os.environ['ELK_SERVICE_ENABLED'] = 1

        print('ELK config successfully created!')