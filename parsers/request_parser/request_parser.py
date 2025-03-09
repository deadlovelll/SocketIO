class RequestParser:
    
    @staticmethod
    def parse_headers (
        self, 
        request: str,
    ) -> dict:
        
        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0].strip()] = parts[1].strip()
        return headers