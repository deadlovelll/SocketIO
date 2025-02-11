class OpenapiDocGenerator:
    
    def serve_ui(self):
        """Generate OpenAPI Specification JSON."""
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Custom API Framework",
                "version": "1.0.0",
                "description": "Auto-generated OpenAPI documentation.",
            },
            "paths": {},
        }

        for path, metadata in self.route_metadata.items():
            method = metadata["method"].lower()
            if path not in openapi_spec["paths"]:
                openapi_spec["paths"][path] = {}

            openapi_spec["paths"][path][method] = {
                "summary": metadata["summary"],
                "description": metadata["description"],
                "responses": {
                    "200": {"description": "Successful response"},
                },
            }

        return openapi_spec