from returnables.html_response.html_response import HTMLResponse
from returnables.json_response.json_response import JsonResponse
import asyncio
from socketio import SocketIO

app = SocketIO()

@app.route("/", methods=['GET'])
def html_response():
    return JsonResponse({'data':'data'})

asyncio.run(app.serve())
