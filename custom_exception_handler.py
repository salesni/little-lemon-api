from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == 401:
            response.data = {'detail': 'Unauthorized access.'}
        elif response.status_code == 403:
            response.data = {'detail': 'Permission denied.'}
        elif response.status_code == 400:
            response.data = {'detail': 'Bad request.'}
        elif response.status_code == 404:
            response.data = {'detail': 'Not found.'}

    return response