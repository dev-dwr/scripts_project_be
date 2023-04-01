from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    exception_class = exc.__class__.__name__
    print(exception_class)
    if exception_class == 'AuthenticationFailed':
        response.data = {
            "error": "Invalid email or password"
        }

    if exception_class == 'NotAuthenticated':
        response.data = {
            "error": "You are not authenticated, please login"
        }

    if exception_class == 'InvalidToken':
        response.data = {
            "error": "Your token expired, please login once again"
        }

    return response
