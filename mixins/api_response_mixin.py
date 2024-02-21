from rest_framework.views import Response
from rest_framework import status

class APIResponseMixin(object):
    def success(self, message: str, status: int = status.HTTP_200_OK, data=None):
        return Response(
            {
                "status": True,
                "message": message,
                "data": data
            }
        )
    
    def error(self, message: str, status: int = status.HTTP_400_BAD_REQUEST, errors=None):
        return Response(
            {
                "status": False,
                "message": message,
                "errors": errors
            },
            status=status
        )
    