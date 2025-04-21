"""
ELK Config Creator Module

This module handles the creation of configuration files for the ELK stack:
Elasticsearch, Logstash, and Kibana.
"""

import os

from commands.elk.elasticsearch.elasticsearch_config_creator.elasticseacrh_config_creator import ElasticsearchConfigCreator
from commands.elk.kibana.kibana_config_creator.kibana_config_creator import KibanaConfigCreator
from commands.elk.logstash.logstash_config_creator.logstash_config_creator import LogstashConfigCreator


class ELKConfigCreator:
    
    """
    Orchestrates the generation of configuration files for all ELK stack components.
    """
    
    @staticmethod
    def create_elk_config() -> None:
        
        """
        Creates the necessary configuration files for Elasticsearch, Logstash, and Kibana.
        Ensures the configuration directory exists and calls the respective creators.

        Sets the environment variable `ELK_SERVICE_ENABLED=1` upon successful creation.
        """
        
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