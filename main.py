from socketio import SocketIO
import asyncio

app = SocketIO()

asyncio.run(app.serve(host="127.0.0.1", port=8000))
