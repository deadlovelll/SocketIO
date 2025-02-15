from socketio.returnables.json_response.json_response import JsonResponse


data = JsonResponse({'key':'value'})
print(type(data))
