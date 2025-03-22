class DockerComposeCreator:
    
    def create_docker_compose_file (
        healthchecks: bool,
        
        postgresql: bool,
        mysql: bool,
        mariadb: bool,
        mongodb: bool,
        cassandra: bool,
        redis: bool,
        
        nginx: bool,
        traefik: bool, #?
        
        elk: bool,
        prometheus: bool,
        grafana: bool,
        jaeger: bool,
        zipking: bool,
        
        rabbitmq: bool,
        celery: bool,
    ) -> str:
        
        pass