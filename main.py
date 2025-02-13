from socketio import SocketIO
import asyncio

app = SocketIO()

@app.route('/')
def home():
    return 'hello world!'

asyncio.run(app.serve())
