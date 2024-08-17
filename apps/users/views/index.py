from django.http import JsonResponse


def index(request):
    data = {
        "message": "Looks like we are up and running!",
    }
    return JsonResponse(data)
