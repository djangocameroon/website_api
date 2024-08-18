from bs4 import BeautifulSoup
from django.core.exceptions import (
    PermissionDenied as DjangoPermissionDenied,
    ValidationError as DjangoValidationError,
    ObjectDoesNotExist, MultipleObjectsReturned,
)
from django.http import Http404
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import (
    ParseError, AuthenticationFailed, NotAuthenticated,
    PermissionDenied as DRFPermissionDenied, NotFound,
    NotAcceptable, UnsupportedMediaType, Throttled,
    MethodNotAllowed, ValidationError as DRFValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def rest_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return _handle_drf_exception(exc, response)

    return _handle_django_exception(exc)


def _handle_drf_exception(exc, response):
    if isinstance(exc, NotFound) or isinstance(exc, Http404):
        response.data = {
            "status": False,
            "message": _("An error occurred while processing your request."),
            "errors": ["This resource was not found."],
            "status_code": response.status_code,
        }
        return response

    errors = _extract_errors_from_response(response)
    response.data = {
        "status": False,
        "message": _('Validation error.') if isinstance(exc, (DjangoValidationError, DRFValidationError)) else _(
            'An error occurred while processing your request.'),
        "errors": errors,
        "status_code": response.status_code,
    }
    return response


def _extract_errors_from_response(response):
    if isinstance(response.data, dict):
        return _flatten_error_dict(response.data)
    elif isinstance(response.data, list):
        return _flatten_error_list(response.data)
    else:
        return [str(response.data)]


def _flatten_error_dict(errors, parent_key=''):
    """
    Recursively flattens nested error dictionaries into a list of strings,
    combining parent keys with child keys, and removing unnecessary indices.
    """
    flat_errors = []
    for key, value in errors.items():
        full_key = parent_key if parent_key else str(key)
        if isinstance(value, list):
            flat_errors.extend(_flatten_error_list(value, full_key))
        elif isinstance(value, dict):
            flat_errors.extend(_flatten_error_dict(value, full_key))
        else:
            flat_errors.append(f"{full_key}: {str(value)}")
    return flat_errors


def _flatten_error_list(errors, parent_key=''):
    """
    Flattens a list of errors, using the parent key and removing unnecessary indices.
    """
    flat_errors = []
    for index, error in enumerate(errors):
        full_key = parent_key
        if isinstance(error, dict):
            flat_errors.extend(_flatten_error_dict(error, full_key))
        else:
            flat_errors.append(f"{full_key}: {str(error)}")
    return flat_errors


def _handle_django_exception(exc):
    status_code = _get_status_code(exc)
    message = _get_default_message(exc)
    errors = _get_errors(exc, message)

    return Response({
        "status": False,
        "message": message,
        "errors": errors,
        "status_code": status_code,
    }, status=status_code)


def _get_status_code(exc):
    exception_status_map = {
        Http404: status.HTTP_404_NOT_FOUND,
        DjangoPermissionDenied: status.HTTP_403_FORBIDDEN,
        DRFPermissionDenied: status.HTTP_403_FORBIDDEN,
        ObjectDoesNotExist: status.HTTP_404_NOT_FOUND,
        MultipleObjectsReturned: status.HTTP_400_BAD_REQUEST,
        ParseError: status.HTTP_400_BAD_REQUEST,
        AuthenticationFailed: status.HTTP_401_UNAUTHORIZED,
        NotAuthenticated: status.HTTP_401_UNAUTHORIZED,
        NotFound: status.HTTP_404_NOT_FOUND,
        MethodNotAllowed: status.HTTP_405_METHOD_NOT_ALLOWED,
        NotAcceptable: status.HTTP_406_NOT_ACCEPTABLE,
        UnsupportedMediaType: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        Throttled: status.HTTP_429_TOO_MANY_REQUESTS,
        ValueError: status.HTTP_400_BAD_REQUEST,
    }
    return exception_status_map.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_default_message(exc):
    default_message_map = {
        Http404: _('Page not found. The requested resource was not found.'),
        (DjangoPermissionDenied, DRFPermissionDenied): _('You do not have permission to perform this action.'),
        ObjectDoesNotExist: _('The requested resource does not exist.'),
        MultipleObjectsReturned: _('Multiple records found. Please contact the administrator.'),
        ParseError: _('The request data could not be parsed.'),
        AuthenticationFailed: _('Please log in to access this resource.'),
        NotAuthenticated: _('You did not provide the necessary credentials.'),
        NotFound: _('This resource was not found.'),
        MethodNotAllowed: _('This method is not allowed.'),
        NotAcceptable: _('The request is not acceptable.'),
        UnsupportedMediaType: _('Please provide a valid media type.'),
        Throttled: _('Request was throttled. Expected available in {0} seconds.'),
    }
    return default_message_map.get(type(exc), _('An unexpected error occurred.'))


def _get_errors(exc, default_message):
    if isinstance(exc, Throttled):
        return [default_message.format(exc.wait)]
    if isinstance(exc, ValueError):
        return [str(exc)]
    if isinstance(exc, Http404) or isinstance(exc, ObjectDoesNotExist):
        return [default_message]
    if isinstance(exc, Exception):
        return [extract_error_from_html(exc)]
    return [default_message]


def extract_error_from_html(exc):
    detail = str(exc)
    if '<html>' in detail.lower():
        try:
            soup = BeautifulSoup(detail, 'html.parser')
            return soup.title.string.strip() if soup.title else _('An unexpected error occurred.')
        except Exception:
            return _('An unexpected error occurred and could not parse the error detail.')
    return detail
