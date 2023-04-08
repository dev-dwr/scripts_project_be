from django.http import JsonResponse

HTTP_500_STATUS_CODE = 500
HTTP_404_STATUS_CODE = 404


def create_json_response(message, status_code):
    response = JsonResponse(data={
        'error': message
    })
    response.status_code = status_code
    return response


def http_500_error_handler(request):
    return create_json_response("Internal Server Error Occurred. Please contact our IT team", HTTP_500_STATUS_CODE)


def http_404_error_handler(request, exception):
    return create_json_response("Provided route not found", HTTP_404_STATUS_CODE)
