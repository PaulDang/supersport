from django.contrib.auth.middleware import get_user


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.current_user = get_user(request)
        response = self.get_response(request)
        return response
