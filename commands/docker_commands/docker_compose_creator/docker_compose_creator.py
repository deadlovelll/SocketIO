class DockerComposeCreator:
    
    def create_docker_compose_file (
        postgresql: bool,
        mongodb: bool,
        cassandra: bool,
        redis: bool,
        
        nginx: bool,
        
        elk: bool,
        elasticsearch: bool,
        kibana: bool,
        logstash: bool,
        prometheus: bool,
        grafana: bool,
        
        rabbitmq: bool,
    ) -> str:
        
        pass