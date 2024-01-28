from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import exception_handler

from exceptions.rest_exception import RestException


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    errors = {}

    if isinstance(exc, RestException):
        return Response(
            {"status": exc.status_code, "message": exc.detail, "errors": errors},
            exc.status_code,
        )

    if response is not None:
        if response.status_code == 500:
            message = _("There was an internal server error please try again later")
        elif response.status_code == 403:
            message = _("Authentication credentials not provided")
        elif response.status_code == 429:
            message = _("Too many requests please try again later")
        elif response.status_code == 400:
            message = _("There as an error in the submited data")
            errors = response.data
        else:
            message = response.status_text

        return Response(
            {"status": response.status_code, "message": message, "errors": errors},
            response.status_code,
        )

    return response
