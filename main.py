from returnables.html_response.html_response import HTMLResponse
from returnables.json_response.json_response import JsonResponse
import asyncio
from socketio import SocketIO

app = SocketIO()

@app.websocket("/ws")
def main(client_socket):
    while True:
        message = app.IORouter.receive_message(client_socket)
        if message:
            print(f"Received: {message}")
            app.IORouter.send_message(client_socket, f"Echo: {message}")
        else:
            break

asyncio.run(app.serve())
