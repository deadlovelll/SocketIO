"""
This module defines the `RequestParser` class for parsing HTTP request data, including request lines and headers.
"""

from typing import Any

class RequestParser:
    
    """
    A class that provides methods for parsing HTTP request data, including request lines and headers.
    """
    
    @staticmethod
    def parse_request (
        request_data: str,
    ) -> tuple[str, dict]:
        
        """
        Parses the HTTP request data into a tuple containing the request line and headers.

        Args:
            request_data (str): The raw HTTP request data as a string.

        Returns:
            tuple[str, dict]: A tuple where the first element is the request line 
                               (e.g., 'GET / HTTP/1.1') and the second is a dictionary 
                               containing the request headers.
        """

        lines = request_data.splitlines()
        request_line = lines[0] if lines else ""
        headers = RequestParser.parse_headers(request_data)
        return request_line, headers

    @staticmethod
    def parse_headers (
        request: str,
    ) -> dict[str, Any]:
        
        """
        Extracts the headers from the given HTTP request data.

        Args:
            request (str): The raw HTTP request data as a string.

        Returns:
            dict: A dictionary where keys are header names and values are the corresponding header values.
        """

        headers = {}
        lines = request.split("\r\n")
        for line in lines[1:]:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0].strip()] = parts[1].strip()
        return headers
