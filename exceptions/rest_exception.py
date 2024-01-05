from rest_framework.exceptions import APIException

class RestException(APIException):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(detail=message)
    
    def __str__(self):
        return self.message