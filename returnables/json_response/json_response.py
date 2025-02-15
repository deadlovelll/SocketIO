import json

class JsonResponse:
        
    def __new__ (
        cls,
        data
    ):
        return json.dumps (
            data,
        )