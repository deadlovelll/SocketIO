from returnables.html_response.html_response import HTMLResponse
from returnables.json_response.json_response import JsonResponse
import asyncio
from socketio import SocketIO

app = SocketIO()

@app.websocket("/")
def main():
    pass

asyncio.run(app.serve())
