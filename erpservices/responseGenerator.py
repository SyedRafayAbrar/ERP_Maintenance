from django.http import JsonResponse

class ResponseGenerator:
    def __init__(self, status, data=None, error=None):
        self.status = status
        self.data = data
        self.error = error

    def generate_response(self):
        response_data = {
            'status': self.status,
        }
        if self.data:
            response_data['data'] = self.data
        else:
            response_data['data'] = None
            
        if self.error:
            response_data['error'] = self.error

        return JsonResponse(response_data)