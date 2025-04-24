"""
This module provides a simple HTTP HTML response wrapper for returning well-formed HTTP responses.
"""

class HTMLResponse:
    
    """
    A basic representation of an HTTP HTML response.

    This class is designed to build raw HTTP response strings with customizable content and status code,
    suitable for use in simple HTTP servers or educational contexts.
    """

    def __init__ (
        self, 
        content: str, 
        status_code: int = 200,
    ) -> None:
        
        """
        Initializes the HTMLResponse with the given HTML content and status code.

        Args:
            content (str): The HTML content to be included in the HTTP response body.
            status_code (int, optional): The HTTP status code to use. Defaults to 200.
        """
        
        self.content = content
        self.status_code = status_code

    def to_http_response (
        self,
    ) -> str:
        
        """
        Converts the response content and status code into a full HTTP response string.

        Returns:
            str: A raw HTTP response string including the status line, headers, and body content.
        """
        
        status_text = "OK" if self.status_code == 200 else "Error"
        status_line = f"HTTP/1.1 {self.status_code} {status_text}\r\n"
        headers = "Content-Type: text/html\r\n\r\n"
        return status_line + headers + self.content
