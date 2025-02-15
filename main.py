from returnables.html_response.html_response import HTMLResponse
import asyncio
from socketio import SocketIO

app = SocketIO()

@app.route("/")
def html_response():
    html_content = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <title>Hello</title>
      </head>
      <body>
        <h1>Hello, world!</h1>
        <p>Welcome to SocketIO.</p>
      </body>
    </html>
    """
    h = HTMLResponse(content=html_content)
    return h.to_http_response()

asyncio.run(app.serve())
