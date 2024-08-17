from typing import Any, Optional, Union, List

from rest_framework import status
from rest_framework.response import Response


class APIResponseMixin:
    """
    A mixin to standardize API responses, providing both success and error response methods.
    """

    def success(
            self, message: str, data: Optional[Any] = None,
            status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """
        Returns a standardized success response.

        :param message: A string message describing the success.
        :param data: Optional data to be included in the response.
        :param status_code: HTTP status code, default is 200 OK.
        :return: DRF Response object with standardized success format.
        """
        response_data = {
            "status": True,
            "message": message,
            "data": data
        }
        return Response(response_data, status=status_code)

    def error(
            self, message: str, errors: Optional[Union[str, List[str]]] = None,
            status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        """
        Returns a standardized error response.

        :param message: A string message describing the error.
        :param errors: Optional error details can be a string or list of strings.
        :param status_code: HTTP status code, default is 400 BAD REQUEST.
        :return: DRF Response object with standardized error format.
        """
        response_data = {
            "status": False,
            "message": message,
            "errors": [errors] if isinstance(errors, str) else errors
        }
        return Response(response_data, status=status_code)
