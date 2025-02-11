class SwaggerDocGenerator:
    def serve_ui(self):
        swagger_ui_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>API Docs</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
                const ui = SwaggerUIBundle({
                    url: '/openapi.json',
                    dom_id: '#swagger-ui',
                });
            </script>
        </body>
        </html>
        """
        return swagger_ui_html