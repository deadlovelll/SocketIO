from socketio import SocketIO
import asyncio

app = SocketIO()

@app.route("/")
async def home():
    return "Hello from custom SocketIO server!"

@app.route("/cpu-bound")
@app.CPUBound("heavy computation")
def cpu_bound_task():
    return "This is a CPU-bound task!"

@app.route("/io-bound")
@app.IOBound("file reading")
def io_bound_task():
    return "This is an IO-bound task!"

asyncio.run(app.serve(host="127.0.0.1", port=8000))
