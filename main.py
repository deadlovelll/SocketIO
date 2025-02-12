from socketio import SocketIO
import asyncio

app = SocketIO()

@app.cache(10)
@app.route('/')
async def home():
    return 9+2

asyncio.run(app.serve(host="127.0.0.1", port=8000))
