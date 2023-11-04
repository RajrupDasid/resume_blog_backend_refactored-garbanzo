
from django.middleware.csrf import get_token


def tokengenerator(request):
    csrf_token = get_token(request)
    response = {
        'intercom': csrf_token,
    }
    return response
