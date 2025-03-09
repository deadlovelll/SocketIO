class RequestParser:
    
    @staticmethod
    def parse_request (
        request_data: str,
    ) -> tuple[str, dict]:

        lines = request_data.splitlines()
        request_line = lines[0] if lines else ""
        headers = RequestParser.parse_headers(request_data)
        return request_line, headers

    @staticmethod
    def parse_headers (
        request: str,
    ) -> dict:

        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0].strip()] = parts[1].strip()
        return headers
