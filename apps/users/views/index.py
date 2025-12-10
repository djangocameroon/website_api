from django.http import JsonResponse


def index(request):
    data = {
        "message": "Looks like we are up and running!",
    }
    return JsonResponse(data)

def page_not_found_view(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'errors': [
            'The resource was not found'
        ]
    })


def server_error_view(request):
    return JsonResponse({
        'status_code': 500,
        'errors': [
            'An error occurred while processing your request',
        ]
    })
