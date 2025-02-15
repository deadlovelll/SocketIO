
class HTMLResponse:
    
    def __init__(self, content: str, status_code: int = 200):
        self.content = content
        self.status_code = status_code

    def to_http_response(self) -> str:
        status_text = "OK" if self.status_code == 200 else "Error"
        status_line = f"HTTP/1.1 {self.status_code} {status_text}\r\n"
        headers = "Content-Type: text/html\r\n\r\n"
        return status_line + headers + self.content
