class ExposedPortsDefiner:
    
    @staticmethod
    def define_exposed_ports (
        ports: list[int], 
        grpc_enabled: bool,
    ) -> str:
        
        ports = "\n".join(f"EXPOSE {port}" for port in ports)
        if grpc_enabled:
            ports += "\nEXPOSE 50051"
        return ports